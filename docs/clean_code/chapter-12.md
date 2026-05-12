# Chương 12: Emergence – Sự nảy sinh trong thiết kế

Chương **Emergence** tập trung vào 4 quy tắc thiết kế đơn giản của Kent Beck. Ý tưởng chính là: thiết kế tốt không nhất thiết phải được tạo ra hoàn hảo ngay từ đầu, mà có thể **nảy sinh dần** thông qua quá trình viết code, viết test và refactor liên tục.

4 quy tắc theo thứ tự ưu tiên:

1. Chạy tất cả các bài kiểm tra
2. Loại bỏ sự trùng lặp
3. Thể hiện rõ ý định
4. Tối giản số lượng lớp và phương thức

---

## Nhận xét nhanh về nội dung tổng hợp

Nội dung ban đầu đã **đúng hướng** với Chương 12 – **Emergence**. Tuy nhiên, có thể chỉnh nhẹ ở vài điểm để tài liệu thực tế hơn khi áp dụng vào Laravel:

1. **“No Duplication” không có nghĩa là xóa mọi dòng code giống nhau**, mà quan trọng hơn là loại bỏ **trùng lặp về kiến thức, nghiệp vụ, quyết định thiết kế**.
2. **“Minimal Classes and Methods” không mâu thuẫn với SRP**. Ý của chương là: đừng tách lớp một cách giáo điều khi chưa có lý do rõ ràng.
3. Với Laravel, nên liên hệ các quy tắc này với: **testability, Form Request, Service/Action class, Eloquent Model, Repository có chọn lọc, Enum, Policy, Validation, Event/Listener**.

---

## 1. Quy tắc 1: Chạy tất cả các bài kiểm tra

Một thiết kế tốt trước hết phải tạo ra hệ thống hoạt động đúng như mong đợi.

Nếu hệ thống không thể kiểm thử, ta không thể tự tin rằng nó đang hoạt động đúng. Vì vậy, khả năng kiểm thử là nền tảng của thiết kế sạch.

Trong Laravel, code khó test thường có các dấu hiệu:

| Dấu hiệu | Vấn đề |
|---|---|
| Gọi trực tiếp `Http::post()` trong controller | Khó fake/mock khi test |
| Gọi trực tiếp `now()` ở nhiều nơi | Khó kiểm soát thời gian trong test |
| Logic nghiệp vụ nằm hết trong controller | Khó unit test |
| Tạo object bằng `new` rải rác | Khó thay thế dependency |
| Query phức tạp lẫn với xử lý nghiệp vụ | Khó đọc, khó kiểm thử |

### Ví dụ chưa tốt

```php
class OrderController extends Controller
{
    public function store(Request $request)
    {
        $order = Order::create([
            'user_id' => auth()->id(),
            'total' => collect($request->items)->sum(fn ($item) => $item['price'] * $item['quantity']),
            'status' => 'pending',
        ]);

        Http::post('https://payment.example.com/charge', [
            'order_id' => $order->id,
            'amount' => $order->total,
        ]);

        return response()->json($order);
    }
}
```

Vấn đề:

- Controller làm quá nhiều việc.
- Tính tổng tiền nằm trong controller.
- Gọi payment trực tiếp nên khó test.
- Nếu muốn test logic tính tổng, phải test qua HTTP/controller.

### Ví dụ tốt hơn

```php
class CreateOrderAction
{
    public function __construct(
        private OrderTotalCalculator $calculator,
        private PaymentGateway $paymentGateway,
    ) {}

    public function execute(User $user, array $items): Order
    {
        $order = Order::create([
            'user_id' => $user->id,
            'total' => $this->calculator->calculate($items),
            'status' => OrderStatus::Pending,
        ]);

        $this->paymentGateway->charge($order);

        return $order;
    }
}
```

Controller trở nên mỏng hơn:

```php
class OrderController extends Controller
{
    public function store(StoreOrderRequest $request, CreateOrderAction $action)
    {
        $order = $action->execute(
            $request->user(),
            $request->validated('items')
        );

        return new OrderResource($order);
    }
}
```

Test dễ hơn:

```php
public function test_it_calculates_order_total(): void
{
    $calculator = new OrderTotalCalculator();

    $total = $calculator->calculate([
        ['price' => 100, 'quantity' => 2],
        ['price' => 50, 'quantity' => 1],
    ]);

    $this->assertEquals(250, $total);
}
```

Ý chính: **khi buộc bản thân viết code có thể test, thiết kế thường sẽ tự nhiên tốt hơn**. Code sẽ có xu hướng nhỏ hơn, ít phụ thuộc hơn và rõ trách nhiệm hơn.

---

## 2. Quy tắc 2: Loại bỏ sự trùng lặp

Sự trùng lặp làm hệ thống khó bảo trì vì khi nghiệp vụ thay đổi, ta phải sửa nhiều nơi. Nếu quên một chỗ, bug sẽ xuất hiện.

Trong Laravel, sự trùng lặp thường xuất hiện ở:

| Loại trùng lặp | Ví dụ |
|---|---|
| Validation lặp lại | Nhiều controller cùng validate `email`, `name`, `password` |
| Query lặp lại | Nhiều nơi cùng viết `where('status', 'active')` |
| Logic trạng thái lặp lại | Nhiều nơi cùng kiểm tra `if ($order->status === 'paid')` |
| Response format lặp lại | Nhiều API tự format JSON giống nhau |
| Permission lặp lại | Nhiều controller tự check quyền bằng `if` |

### Ví dụ 1: Loại bỏ duplication bằng Form Request

Chưa tốt:

```php
class StoreProductController extends Controller
{
    public function __invoke(Request $request)
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'price' => ['required', 'numeric', 'min:0'],
            'sku' => ['required', 'string', 'unique:products,sku'],
        ]);

        Product::create($data);

        return response()->json(['message' => 'Product created']);
    }
}
```

```php
class UpdateProductController extends Controller
{
    public function __invoke(Request $request, Product $product)
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'price' => ['required', 'numeric', 'min:0'],
            'sku' => ['required', 'string', 'unique:products,sku,' . $product->id],
        ]);

        $product->update($data);

        return response()->json(['message' => 'Product updated']);
    }
}
```

Logic validate bị lặp.

Tốt hơn:

```php
class StoreProductRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'price' => ['required', 'numeric', 'min:0'],
            'sku' => ['required', 'string', 'unique:products,sku'],
        ];
    }
}
```

```php
class UpdateProductRequest extends FormRequest
{
    public function rules(): array
    {
        $productId = $this->route('product')->id;

        return [
            'name' => ['required', 'string', 'max:255'],
            'price' => ['required', 'numeric', 'min:0'],
            'sku' => ['required', 'string', 'unique:products,sku,' . $productId],
        ];
    }
}
```

Controller sạch hơn:

```php
class StoreProductController extends Controller
{
    public function __invoke(StoreProductRequest $request)
    {
        Product::create($request->validated());

        return response()->json(['message' => 'Product created']);
    }
}
```

---

### Ví dụ 2: Loại bỏ duplication bằng Eloquent Scope

Chưa tốt:

```php
$activeUsers = User::where('status', 'active')->get();

$activeAdmins = User::where('status', 'active')
    ->where('role', 'admin')
    ->get();

$activeCustomers = User::where('status', 'active')
    ->where('role', 'customer')
    ->get();
```

Tốt hơn:

```php
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('status', UserStatus::Active);
    }
}
```

Sử dụng:

```php
$activeUsers = User::active()->get();

$activeAdmins = User::active()
    ->where('role', 'admin')
    ->get();

$activeCustomers = User::active()
    ->where('role', 'customer')
    ->get();
```

Điểm tốt ở đây không chỉ là code ngắn hơn, mà là logic “active user là gì” được gom về một nơi.

---

### Ví dụ 3: Loại bỏ duplication bằng Service/Action

Chưa tốt:

```php
class OrderController extends Controller
{
    public function cancel(Order $order)
    {
        if ($order->status === 'paid') {
            throw new Exception('Paid order cannot be cancelled');
        }

        $order->status = 'cancelled';
        $order->cancelled_at = now();
        $order->save();

        Mail::to($order->user)->send(new OrderCancelledMail($order));

        return response()->json(['message' => 'Order cancelled']);
    }
}
```

Sau đó ở admin cũng có logic tương tự:

```php
class AdminOrderController extends Controller
{
    public function cancel(Order $order)
    {
        if ($order->status === 'paid') {
            throw new Exception('Paid order cannot be cancelled');
        }

        $order->status = 'cancelled';
        $order->cancelled_at = now();
        $order->save();

        Mail::to($order->user)->send(new OrderCancelledMail($order));

        return response()->json(['message' => 'Order cancelled by admin']);
    }
}
```

Tốt hơn:

```php
class CancelOrderAction
{
    public function execute(Order $order): void
    {
        if ($order->isPaid()) {
            throw new CannotCancelPaidOrderException();
        }

        $order->update([
            'status' => OrderStatus::Cancelled,
            'cancelled_at' => now(),
        ]);

        Mail::to($order->user)->send(new OrderCancelledMail($order));
    }
}
```

Model thể hiện nghiệp vụ rõ hơn:

```php
class Order extends Model
{
    public function isPaid(): bool
    {
        return $this->status === OrderStatus::Paid;
    }
}
```

Controller:

```php
class OrderController extends Controller
{
    public function cancel(Order $order, CancelOrderAction $action)
    {
        $action->execute($order);

        return response()->json(['message' => 'Order cancelled']);
    }
}
```

---

## 3. Quy tắc 3: Tính biểu đạt

Code tốt không chỉ chạy đúng, mà còn phải **nói rõ ý định**.

Trong Laravel, tính biểu đạt thường đến từ:

| Kỹ thuật | Ví dụ |
|---|---|
| Đặt tên rõ nghĩa | `CancelOrderAction`, `ApproveInvoiceAction` |
| Dùng Enum | `OrderStatus::Paid` thay vì `'paid'` |
| Dùng method nghiệp vụ | `$order->isPaid()` thay vì so sánh string |
| Dùng Form Request | `StoreProductRequest` nói rõ request dùng để làm gì |
| Dùng Policy | `$this->authorize('update', $post)` rõ hơn tự viết `if` |
| Dùng Resource | `OrderResource` thể hiện rõ output API |

### Ví dụ chưa tốt

```php
if ($order->status === 'p' && $order->payment_status === 'ok') {
    $order->status = 's';
    $order->save();
}
```

Code này khó hiểu vì:

- `'p'` là gì?
- `'ok'` là gì?
- `'s'` là gì?
- Điều kiện này đại diện cho nghiệp vụ nào?

### Ví dụ tốt hơn

```php
if ($order->isReadyToShip()) {
    $order->markAsShipping();
}
```

Trong model:

```php
class Order extends Model
{
    public function isReadyToShip(): bool
    {
        return $this->status === OrderStatus::Paid
            && $this->payment_status === PaymentStatus::Confirmed;
    }

    public function markAsShipping(): void
    {
        $this->update([
            'status' => OrderStatus::Shipping,
        ]);
    }
}
```

Dùng Enum:

```php
enum OrderStatus: string
{
    case Pending = 'pending';
    case Paid = 'paid';
    case Shipping = 'shipping';
    case Cancelled = 'cancelled';
}
```

Code sau khi refactor đọc gần giống ngôn ngữ nghiệp vụ:

```php
if ($order->isReadyToShip()) {
    $order->markAsShipping();
}
```

Đây chính là **expressive code**.

---

## 4. Quy tắc 4: Tối giản lớp và phương thức

Quy tắc này nhắc rằng: chia nhỏ là tốt, nhưng chia quá mức cũng có thể làm hệ thống phức tạp.

Trong Laravel, lỗi phổ biến là tạo quá nhiều lớp theo kiểu máy móc:

```text
ProductController
ProductService
ProductRepositoryInterface
ProductRepository
ProductDTO
ProductMapper
ProductFactory
ProductAction
ProductValidator
```

Nếu nghiệp vụ chỉ là CRUD đơn giản, cấu trúc này có thể là quá mức cần thiết.

### Ví dụ over-engineering

```php
interface ProductRepositoryInterface
{
    public function create(array $data): Product;
}
```

```php
class ProductRepository implements ProductRepositoryInterface
{
    public function create(array $data): Product
    {
        return Product::create($data);
    }
}
```

```php
class ProductService
{
    public function __construct(
        private ProductRepositoryInterface $products
    ) {}

    public function createProduct(array $data): Product
    {
        return $this->products->create($data);
    }
}
```

Nếu chỉ gọi `Product::create($data)`, thì repository và service chưa mang lại nhiều giá trị.

### Cách đơn giản hơn

```php
class ProductController extends Controller
{
    public function store(StoreProductRequest $request)
    {
        $product = Product::create($request->validated());

        return new ProductResource($product);
    }
}
```

Cách này đủ tốt nếu nghiệp vụ đơn giản.

---

### Khi nào nên tách Action/Service?

Nên tách khi logic bắt đầu có nhiều bước nghiệp vụ:

```php
class CreateOrderAction
{
    public function __construct(
        private OrderTotalCalculator $calculator,
        private InventoryService $inventory,
        private PaymentGateway $paymentGateway,
    ) {}

    public function execute(User $user, array $items): Order
    {
        $order = Order::create([
            'user_id' => $user->id,
            'total' => $this->calculator->calculate($items),
            'status' => OrderStatus::Pending,
        ]);

        $this->inventory->reserve($order);
        $this->paymentGateway->charge($order);

        return $order;
    }
}
```

Ở đây việc tách `CreateOrderAction` là hợp lý vì use case có nhiều bước:

1. Tạo order
2. Tính tổng tiền
3. Giữ hàng trong kho
4. Gọi thanh toán
5. Cập nhật trạng thái

Nếu để toàn bộ trong controller, controller sẽ phình to và khó test.

---

## Bảng tổng hợp áp dụng trong Laravel

| Quy tắc | Ý nghĩa | Áp dụng trong Laravel |
|---|---|---|
| Runs All the Tests | Code phải kiểm thử được | Tách logic khỏi controller, dùng DI, fake mail/job/http |
| No Duplication | Không lặp lại kiến thức nghiệp vụ | Form Request, Scope, Action, Enum, Policy |
| Expressive | Code phải nói rõ ý định | Tên class/method rõ, Enum, method nghiệp vụ như `isPaid()` |
| Minimal Classes and Methods | Không tạo lớp dư thừa | Không lạm dụng Repository/Interface cho CRUD đơn giản |

---

## Checklist review code theo Chương 12

Khi review một đoạn code Laravel, có thể hỏi:

| Câu hỏi | Mục đích |
|---|---|
| Code này có test được không? | Kiểm tra quy tắc 1 |
| Logic nghiệp vụ có bị lặp ở nhiều nơi không? | Kiểm tra quy tắc 2 |
| Tên class/method có nói rõ ý định không? | Kiểm tra quy tắc 3 |
| Có magic string như `'paid'`, `'active'`, `'done'` không? | Kiểm tra tính biểu đạt |
| Có đang tạo quá nhiều Service/Repository/Interface không cần thiết không? | Kiểm tra quy tắc 4 |
| Nếu xóa bớt một lớp, code có dễ hiểu hơn không? | Tránh over-engineering |
| Nếu thêm test, có phải mock quá nhiều thứ không? | Dấu hiệu coupling cao |
| Controller có chứa quá nhiều nghiệp vụ không? | Dấu hiệu cần tách Action/Service |

---

## Kết luận

Chương **Emergence** nhấn mạnh rằng thiết kế sạch có thể nảy sinh dần thông qua vòng lặp: viết code, chạy test, phát hiện mùi thiết kế, rồi refactor. Bốn quy tắc của Kent Beck giúp lập trình viên giữ thiết kế đơn giản nhưng vẫn chắc chắn: hệ thống phải chạy đúng qua test, không có trùng lặp không cần thiết, thể hiện rõ ý định, và không tạo thêm lớp/phương thức dư thừa.

Trong Laravel, các quy tắc này có thể được áp dụng thông qua việc tách logic nghiệp vụ khỏi controller, sử dụng Form Request, Enum, Eloquent Scope, Policy, Action/Service class khi cần, đồng thời tránh lạm dụng Repository hoặc Interface cho những trường hợp CRUD đơn giản.
