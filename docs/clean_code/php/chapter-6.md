# Clean Code - Chương 6 - Đối tượng và cấu trúc dữ liệu

## 1. Nội dung cốt lõi của chương

### 1.1 Trừu tượng hóa dữ liệu (Data Abstraction)

#### a. Tại sao phải trừu tượng hóa dữ liệu?

Trừu tượng hóa dữ liệu là quá trình ẩn đi chi tiết thực thi và chỉ cung cấp những phương thức cần thiết để tương tác với dữ liệu đó.
Việc này không chỉ đơn thuần là đặt một lớp hàm getter/setter giữa các biến.

```php
class Order
{
    private float $total;
    private string $status;

    public function getTotal(): float
    {
        return $this->total;
    }

    public function setStatus(string $status): void
    {
        $this->status = $status;
    }
}
```

Cách tiếp cận trên chưa tốt vì nó không thực sự trừu tượng hóa dữ liệu.
Các phương thức getter/setter chỉ đơn giản là cung cấp quyền truy cập trực tiếp đến các thuộc tính, mà không kiểm soát được cách chúng được sử dụng.
Bên ngoài lớp, vẫn biết chi tiết về chi tiết dữ liệu, ở đây là setStatus('paid') hoặc setStatus('canceled').

Cách tốt hơn

```php
class Order
{
    const STATUS_PAID = 'paid';
    const STATUS_PENDING = 'pending';
    const STATUS_CANCELED = 'canceled';

    public function markAsPaid(): void
    {
        if ($this->status !== self::STATUS_PENDING) {
            throw new InvalidArgumentException('Only pending orders can be marked as paid.');
        }

        $this->status = self::STATUS_PAID;
        // Additional logic related to marking the order as paid can be added here
    }

    public function cancel(): void
    {
        if ($this->status === self::STATUS_PAID) {
            throw new InvalidArgumentException('Paid orders cannot be canceled.');
        }

        $this->status = 'canceled';
        // Additional logic related to canceling the order can be added here
    }
}
```

Cách tiếp cận này tốt hơn vì nó ẩn đi chi tiết về cách trạng thái của đơn hàng được quản lý.
Bên ngoài lớp, chỉ biết rằng có thể gọi markAsPaid() hoặc cancel(), mà không cần biết chi tiết về cách trạng thái được thay đổi.
Điều này giúp giảm sự phụ thuộc vào chi tiết dữ liệu và làm cho mã dễ bảo trì hơn.

### 1.2 Tính bất đối xứng giữa dữ liệu và đối tượng

#### a. Dữ liệu

- Đặc điểm: Phơi bày dữ liệu trực tiếp và không có hành vi (behavior).
- Ưu điểm: Dễ dàng thêm các hàm mới mà không cần thay đổi cấu trúc dữ liệu hiện có.
- Nhược điểm: Khó thêm các loại dữ liệu mới vì tất cả các hàm hiện có phải được thay đổi để hỗ trợ loại dữ liệu mới.

Ví dụ:

```php
class ProductFilterData
{
    public function __construct(
        public readonly ?string $keyword,
        public readonly ?int $categoryId,
        public readonly ?float $minPrice,
        public readonly ?float $maxPrice,
        public readonly ?string $sortBy,
    ) {}

    public static function fromRequest(Request $request): self
    {
        return new self(
            keyword: $request->input('keyword'),
            categoryId: $request->integer('category_id') ?: null,
            minPrice: $request->filled('min_price')
                ? (float) $request->input('min_price')
                : null,
            maxPrice: $request->filled('max_price')
                ? (float) $request->input('max_price')
                : null,
            sortBy: $request->input('sort_by'),
        );
    }
}

class ProductSearchAction {
    public function execute(ProductFilterData $filterData)
    {
        return Product::query()
            ->when($filter->keyword, function ($query) use ($filter) {
                $query->where('name', 'like', "%{$filter->keyword}%");
            })
            ->when($filter->categoryId, function ($query) use ($filter) {
                $query->where('category_id', $filter->categoryId);
            })
            ->when($filter->minPrice, function ($query) use ($filter) {
                $query->where('price', '>=', $filter->minPrice);
            })
            ->when($filter->maxPrice, function ($query) use ($filter) {
                $query->where('price', '<=', $filter->maxPrice);
            })
            ->when($filter->sortBy, function ($query) use ($filter) {
                $query->orderBy($filter->sortBy);
            })
            ->paginate();
    }
}

class ProductController {
    public function index(Request $request, ProductSearchAction $action)
    {
        $filterData = ProductFilterData::fromRequest($request);
        $products = $action->execute($filterData);

        // Return response with products
    }
}

```

Ưu điểm của cách tiếp cận này là dễ dàng thêm các hàm mới.
Ví dụ ta muốn xuất (export) sản phẩm ra file CSV, chỉ cần thêm một class `ProductExportAction` mà không cần thay đổi cấu trúc dữ liệu `ProductFilterData` hiện có.

```php
class ProductExportAction {
    public function execute(ProductFilterData $filterData)
    {
        $products = Product::query()
            ->when($filter->keyword, function ($query) use ($filter) {
                $query->where('name', 'like', "%{$filter->keyword}%");
            })
            ->when($filter->categoryId, function ($query) use ($filter) {
                $query->where('category_id', $filter->categoryId);
            })
            // ... (same filtering logic as ProductFilterAction)
            ->get();
        // Logic to export $products to CSV
    }
}
```

Tuy nhiên, nhược điểm của cách tiếp cận này là khó thêm các loại dữ liệu mới.
Nếu ta muốn thêm một loại dữ liệu mới nếu có nhiều service đang sử dụng.
Ví dụ nếu muốn thêm một trường `brandId` vào `ProductFilterData`, tất cả các service đang sử dụng `ProductFilterData` đều phải được thay đổi để hỗ trợ trường mới này.

```php
class ProductFilterData
{
    public function __construct(
        public readonly ?string $keyword,
        public readonly ?int $categoryId,
        public readonly ?float $minPrice,
        public readonly ?float $maxPrice,
        public readonly ?string $sortBy,
        public readonly ?int $brandId, // New field added
    ) {}

    // ... (same fromRequest method)
}
```

Các service sử dụng `ProductFilterData` cũng phải được thay đổi

```php
ProductSearchAction
ProductExportAction
```

#### b. Đối tượng (Object)

- Đặc điểm: Ẩn dữ liệu và cung cấp các hàm để tương tác với dữ liệu đó.
- Ưu điểm: Dễ thêm các loại đối tượng mới mà không cần thay đổi các hàm hiện có.
- Nhược điểm: Khó thêm các hàm mới vì tất cả các class hiện có phải được thay đổi để hỗ trợ hàm mới.

Ví dụ:

```php
class Product extends Model {
    public function publish(): void
    {
        // Logic to publish the product
    }

    public function applyDiscount(): void
    {
        // Logic to archive the product
    }
}
```

### b. Tính bất đối xứng giữa dữ liệu và đối tượng

Ví dụ về cấu trúc dữ liệu:

```php
class CreateOrderData
{
    public function __construct(
        public int $userId,
        public array $items,
        public string $paymentMethod
    ) {}
}
```


### 1.3 Nguyên tác Demeter

### 1.4 Đối tượng truyền dữ liệu
