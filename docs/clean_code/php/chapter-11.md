# Clean Code – Chương Systems: Ví dụ Laravel

## 1. Tách biệt việc xây dựng hệ thống khỏi việc sử dụng

Trong Laravel, phần “xây dựng hệ thống” thường nằm ở:

- `ServiceProvider`
- Laravel Service Container
- file cấu hình `config/*.php`
- binding interface với implementation

Logic nghiệp vụ không nên tự khởi tạo dependency bằng `new`.

### Cách chưa tốt: Service tự tạo dependency

```php
class OrderService
{
    private PaymentGateway $paymentGateway;

    public function __construct()
    {
        $this->paymentGateway = new StripePaymentGateway();
    }

    public function checkout(Order $order): void
    {
        $this->paymentGateway->charge($order->total);
    }
}
```

#### Vấn đề

`OrderService` đang có hai trách nhiệm:

1. Xử lý nghiệp vụ checkout.
2. Biết cách tạo `StripePaymentGateway`.

Điều này làm code khó test, khó thay đổi sang gateway khác như PayPal, VNPay, MoMo.

### Cách tốt hơn: Dùng Dependency Injection

```php
interface PaymentGateway
{
    public function charge(int $amount): void;
}
```

```php
class StripePaymentGateway implements PaymentGateway
{
    public function charge(int $amount): void
    {
        // Gọi API Stripe
    }
}
```

```php
class OrderService
{
    public function __construct(
        private PaymentGateway $paymentGateway
    ) {}

    public function checkout(Order $order): void
    {
        $this->paymentGateway->charge($order->total);
    }
}
```

Binding trong `AppServiceProvider`:

```php
use App\Contracts\PaymentGateway;
use App\Services\StripePaymentGateway;

public function register(): void
{
    $this->app->bind(PaymentGateway::class, StripePaymentGateway::class);
}
```

#### Ý nghĩa theo Clean Code

`OrderService` chỉ sử dụng dependency, không tự xây dựng dependency.

Laravel Service Container đóng vai trò giống phần `main`, nơi hệ thống được lắp ráp trước khi chạy.

---

## 2. Sử dụng Factory khi ứng dụng cần kiểm soát thời điểm tạo object

Có trường hợp object chỉ được tạo khi runtime có đủ dữ liệu, ví dụ chọn cổng thanh toán theo phương thức người dùng chọn.

### Cách chưa tốt

```php
class PaymentService
{
    public function pay(Order $order, string $method): void
    {
        if ($method === 'stripe') {
            $gateway = new StripePaymentGateway();
        } elseif ($method === 'paypal') {
            $gateway = new PaypalPaymentGateway();
        } else {
            throw new InvalidArgumentException('Unsupported payment method');
        }

        $gateway->charge($order->total);
    }
}
```

#### Vấn đề

`PaymentService` bị dính logic khởi tạo object.

### Cách tốt hơn: Tách Factory

```php
class PaymentGatewayFactory
{
    public function make(string $method): PaymentGateway
    {
        return match ($method) {
            'stripe' => app(StripePaymentGateway::class),
            'paypal' => app(PaypalPaymentGateway::class),
            default => throw new InvalidArgumentException('Unsupported payment method'),
        };
    }
}
```

```php
class PaymentService
{
    public function __construct(
        private PaymentGatewayFactory $factory
    ) {}

    public function pay(Order $order, string $method): void
    {
        $gateway = $this->factory->make($method);

        $gateway->charge($order->total);
    }
}
```

#### Ý nghĩa

`PaymentService` vẫn quyết định **khi nào** cần tạo gateway, nhưng không biết chi tiết **tạo như thế nào**.

Đây là tinh thần của Factory trong chương Systems.

---

## 3. Mở rộng hệ thống bằng Separation of Concerns

Trong Laravel, các vấn đề như authentication, authorization, validation, transaction, logging, cache không nên trộn trực tiếp vào logic nghiệp vụ chính.

### Cách chưa tốt: Controller làm quá nhiều việc

```php
class OrderController extends Controller
{
    public function store(Request $request)
    {
        if (! auth()->user()->can('create', Order::class)) {
            abort(403);
        }

        $data = $request->validate([
            'product_id' => ['required', 'exists:products,id'],
            'quantity' => ['required', 'integer', 'min:1'],
        ]);

        DB::beginTransaction();

        try {
            $product = Product::findOrFail($data['product_id']);

            if ($product->stock < $data['quantity']) {
                throw new Exception('Not enough stock');
            }

            $order = Order::create([
                'user_id' => auth()->id(),
                'product_id' => $product->id,
                'quantity' => $data['quantity'],
                'total' => $product->price * $data['quantity'],
            ]);

            $product->decrement('stock', $data['quantity']);

            Log::info('Order created', ['order_id' => $order->id]);

            DB::commit();

            return response()->json($order);
        } catch (Throwable $e) {
            DB::rollBack();

            throw $e;
        }
    }
}
```

#### Vấn đề

Controller đang xử lý quá nhiều concern:

- Authorization
- Validation
- Transaction
- Business logic
- Logging
- Database operation
- HTTP response

### Cách tốt hơn: Tách concern

#### Form Request xử lý validation

```php
class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'product_id' => ['required', 'exists:products,id'],
            'quantity' => ['required', 'integer', 'min:1'],
        ];
    }
}
```

#### Action xử lý nghiệp vụ

```php
class CreateOrderAction
{
    public function execute(User $user, array $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $product = Product::findOrFail($data['product_id']);

            if ($product->stock < $data['quantity']) {
                throw new NotEnoughStockException();
            }

            $order = Order::create([
                'user_id' => $user->id,
                'product_id' => $product->id,
                'quantity' => $data['quantity'],
                'total' => $product->price * $data['quantity'],
            ]);

            $product->decrement('stock', $data['quantity']);

            return $order;
        });
    }
}
```

#### Controller trở nên mỏng

```php
class OrderController extends Controller
{
    public function store(
        StoreOrderRequest $request,
        CreateOrderAction $createOrder
    ) {
        $order = $createOrder->execute(
            $request->user(),
            $request->validated()
        );

        return response()->json($order);
    }
}
```

#### Ý nghĩa

Controller chỉ còn nhiệm vụ điều phối HTTP request/response.

Validation nằm trong `FormRequest`.

Authorization nằm trong `authorize()` hoặc `Policy`.

Business logic nằm trong `Action`.

Transaction được gom lại trong use case chính.

Đây là cách Laravel hỗ trợ Separation of Concerns rất tự nhiên.

---

## 4. Cross-Cutting Concerns trong Laravel

Cross-cutting concerns là những vấn đề xuất hiện ở nhiều nơi trong hệ thống, ví dụ:

| Concern | Laravel thường xử lý bằng |
|---|---|
| Authentication | Middleware |
| Authorization | Policy / Gate |
| Validation | Form Request |
| Logging | Middleware / Event Listener / Decorator |
| Cache | Decorator / Repository / Service |
| Transaction | Action / Service / Unit of Work |
| Rate limit | Middleware |
| Queue | Job / Listener |

### Ví dụ: Logging không nên nằm rải rác trong business logic

#### Cách chưa tốt

```php
class CreateOrderAction
{
    public function execute(User $user, array $data): Order
    {
        Log::info('Start creating order');

        $order = Order::create([
            // ...
        ]);

        Log::info('Order created', [
            'order_id' => $order->id,
        ]);

        return $order;
    }
}
```

#### Cách tốt hơn: Dùng Event

```php
class CreateOrderAction
{
    public function execute(User $user, array $data): Order
    {
        $order = Order::create([
            // ...
        ]);

        event(new OrderCreated($order));

        return $order;
    }
}
```

```php
class LogOrderCreated
{
    public function handle(OrderCreated $event): void
    {
        Log::info('Order created', [
            'order_id' => $event->order->id,
        ]);
    }
}
```

#### Ý nghĩa

`CreateOrderAction` không cần biết hệ thống sẽ log, gửi email, gửi notification hay dispatch job gì sau khi order được tạo.

Nó chỉ phát ra một sự kiện nghiệp vụ: `OrderCreated`.

---

## 5. Logic nghiệp vụ thuần túy, tránh phụ thuộc framework quá sâu

Trong Clean Code, chương Systems khuyên logic nghiệp vụ nên càng “thuần” càng tốt.

Trong Laravel, điều này có nghĩa là không phải logic nào cũng nên đặt hết vào Controller, Model hoặc Facade.

### Cách chưa tốt: Logic nghiệp vụ bị dính vào Eloquent Model

```php
class Order extends Model
{
    public function calculateTotal(): int
    {
        $total = 0;

        foreach ($this->items as $item) {
            $total += $item->price * $item->quantity;
        }

        if ($this->user->is_vip) {
            $total *= 0.9;
        }

        return (int) $total;
    }
}
```

#### Vấn đề

Model vừa đại diện database, vừa chứa nhiều logic tính toán.

Nếu logic tính giá phức tạp hơn, `Order` sẽ ngày càng phình to.

### Cách tốt hơn: Tách Domain Service thuần PHP

```php
class OrderTotalCalculator
{
    public function calculate(array $items, bool $isVip): int
    {
        $total = 0;

        foreach ($items as $item) {
            $total += $item['price'] * $item['quantity'];
        }

        if ($isVip) {
            $total = (int) ($total * 0.9);
        }

        return $total;
    }
}
```

Sử dụng trong Laravel Action:

```php
class CreateOrderAction
{
    public function __construct(
        private OrderTotalCalculator $calculator
    ) {}

    public function execute(User $user, array $data): Order
    {
        $total = $this->calculator->calculate(
            $data['items'],
            $user->is_vip
        );

        return Order::create([
            'user_id' => $user->id,
            'total' => $total,
        ]);
    }
}
```

#### Ý nghĩa

`OrderTotalCalculator` là class thuần PHP.

Nó không phụ thuộc Laravel, không phụ thuộc Eloquent, không gọi Facade.

Vì vậy, nó dễ unit test hơn.

```php
public function test_it_applies_vip_discount(): void
{
    $calculator = new OrderTotalCalculator();

    $total = $calculator->calculate([
        ['price' => 100_000, 'quantity' => 2],
    ], true);

    $this->assertSame(180_000, $total);
}
```

---

## 6. Proxy / Decorator trong Laravel

Laravel không dùng AOP mạnh như một số framework Java, nhưng ta có thể dùng Decorator để bọc thêm behavior như cache, log, retry, metric.

### Ví dụ: Bọc service bằng Cache Decorator

Interface:

```php
interface ProductReader
{
    public function findById(int $id): Product;
}
```

Service thật:

```php
class EloquentProductReader implements ProductReader
{
    public function findById(int $id): Product
    {
        return Product::findOrFail($id);
    }
}
```

Decorator thêm cache:

```php
class CachedProductReader implements ProductReader
{
    public function __construct(
        private ProductReader $inner
    ) {}

    public function findById(int $id): Product
    {
        return cache()->remember(
            "products.$id",
            now()->addMinutes(10),
            fn () => $this->inner->findById($id)
        );
    }
}
```

Binding trong Service Provider:

```php
public function register(): void
{
    $this->app->bind(EloquentProductReader::class);

    $this->app->bind(ProductReader::class, function ($app) {
        return new CachedProductReader(
            $app->make(EloquentProductReader::class)
        );
    });
}
```

#### Ý nghĩa

Business code chỉ phụ thuộc vào `ProductReader`.

Nó không cần biết dữ liệu đang được lấy trực tiếp từ database hay từ cache.

---

## 7. Trì hoãn quyết định kiến trúc

Một hệ thống Laravel sạch không cần quyết định quá sớm mọi thứ ngay từ đầu.

Ví dụ, ban đầu bạn có thể dùng local storage:

```php
Storage::disk('local')->put($path, $content);
```

Nhưng nếu code nghiệp vụ gọi trực tiếp `Storage::disk('local')` ở khắp nơi, sau này chuyển sang S3 sẽ khó.

### Cách tốt hơn: Tạo abstraction

```php
interface FileStorage
{
    public function put(string $path, string $content): void;
}
```

```php
class LaravelFileStorage implements FileStorage
{
    public function put(string $path, string $content): void
    {
        Storage::put($path, $content);
    }
}
```

```php
class UploadDocumentAction
{
    public function __construct(
        private FileStorage $storage
    ) {}

    public function execute(UploadedFile $file): void
    {
        $this->storage->put(
            'documents/' . $file->hashName(),
            $file->getContent()
        );
    }
}
```

Binding:

```php
public function register(): void
{
    $this->app->bind(FileStorage::class, LaravelFileStorage::class);
}
```

#### Ý nghĩa

Hôm nay có thể dùng local storage.

Sau này có thể đổi sang S3, MinIO hoặc self-hosted storage mà không làm thay đổi business logic.

Đây là ví dụ của việc trì hoãn quyết định kỹ thuật đến khi thật sự cần.

---

## 8. Sử dụng tiêu chuẩn một cách khôn ngoan

Laravel có nhiều convention tốt, nhưng không nên áp dụng máy móc.

Ví dụ: không phải lúc nào cũng cần Repository Pattern.

### Khi không cần Repository

Nếu chỉ CRUD đơn giản:

```php
class ProductController extends Controller
{
    public function show(Product $product)
    {
        return response()->json($product);
    }
}
```

Việc thêm `ProductRepository` trong trường hợp này có thể làm hệ thống phức tạp không cần thiết.

### Khi Repository có ích

Repository có ích khi logic truy vấn phức tạp hoặc cần che giấu nguồn dữ liệu.

```php
interface ProductRepository
{
    public function findAvailableForSale(int $id): Product;
}
```

```php
class EloquentProductRepository implements ProductRepository
{
    public function findAvailableForSale(int $id): Product
    {
        return Product::query()
            ->where('id', $id)
            ->where('is_active', true)
            ->where('stock', '>', 0)
            ->firstOrFail();
    }
}
```

#### Ý nghĩa

Không nên dùng pattern chỉ vì “chuẩn”.

Chỉ dùng khi nó giải quyết vấn đề thật sự: testability, thay đổi nguồn dữ liệu, truy vấn phức tạp, hoặc giảm phụ thuộc framework.

---

## 9. DSL trong Laravel

Laravel có nhiều DSL tự nhiên giúp code gần với ngôn ngữ nghiệp vụ hơn.

Ví dụ validation rule:

```php
public function rules(): array
{
    return [
        'email' => ['required', 'email'],
        'quantity' => ['required', 'integer', 'min:1'],
        'payment_method' => ['required', Rule::in(['stripe', 'paypal'])],
    ];
}
```

Query Builder cũng là một dạng DSL:

```php
Order::query()
    ->whereBelongsTo($user)
    ->where('status', OrderStatus::Paid)
    ->whereDate('created_at', today())
    ->latest()
    ->get();
```

### Ví dụ DSL nghiệp vụ bằng method rõ nghĩa

Thay vì viết:

```php
if ($order->status === 'paid' && $order->shipped_at === null) {
    // ship order
}
```

Có thể viết:

```php
if ($order->isReadyToShip()) {
    // ship order
}
```

Trong model:

```php
class Order extends Model
{
    public function isReadyToShip(): bool
    {
        return $this->status === OrderStatus::Paid
            && $this->shipped_at === null;
    }
}
```

#### Ý nghĩa

Code đọc gần với ngôn ngữ nghiệp vụ hơn:

> Nếu đơn hàng đã sẵn sàng giao, thì tiến hành giao hàng.

Thay vì bắt người đọc phải hiểu nhiều điều kiện kỹ thuật.

---

## 10. Tổng kết theo Laravel

| Ý tưởng trong Clean Code | Áp dụng trong Laravel |
|---|---|
| Tách xây dựng khỏi sử dụng | Service Container, Service Provider, config |
| Dependency Injection | Constructor injection, interface binding |
| Factory | Tạo object theo runtime condition |
| Separation of Concerns | Controller mỏng, FormRequest, Policy, Action, Service |
| Cross-cutting concerns | Middleware, Event, Listener, Job, Decorator |
| Logic thuần túy | Domain Service, DTO, Value Object |
| Proxy / AOP | Decorator, Middleware, Pipeline |
| Trì hoãn quyết định | Interface cho payment, storage, notification, search |
| Dùng tiêu chuẩn khôn ngoan | Không lạm dụng Repository/Service nếu chưa cần |
| DSL | Validation rules, Query Builder, method nghiệp vụ rõ nghĩa |

---

## Checklist review nhanh cho Laravel Systems

| Câu hỏi review | Ý nghĩa |
|---|---|
| Class này có tự `new` dependency không? | Nếu có, cân nhắc DI |
| Logic khởi tạo object có nằm lẫn trong business logic không? | Nếu có, cân nhắc Factory hoặc Service Provider |
| Controller có đang xử lý quá nhiều việc không? | Nếu có, tách FormRequest, Action, Policy |
| Logic nghiệp vụ có phụ thuộc quá sâu vào Laravel Facade không? | Nếu có, cân nhắc abstraction |
| Logging, cache, notification có nằm rải rác trong use case không? | Nếu có, cân nhắc Event, Listener, Decorator |
| Có đang dùng pattern chỉ vì “chuẩn” không? | Chỉ dùng khi có giá trị rõ ràng |
| Code có đọc giống ngôn ngữ nghiệp vụ không? | Nếu không, cân nhắc đặt method rõ nghĩa hơn |
| Có quyết định kỹ thuật nào đang bị khóa quá sớm không? | Dùng interface để trì hoãn quyết định |
