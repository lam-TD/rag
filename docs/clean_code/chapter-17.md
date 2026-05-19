# Clean Code – Chương 17: Smells and Heuristics

> Tài liệu tổng hợp dành cho người học, diễn giải lại bằng ngôn ngữ riêng kèm ví dụ **PHP 8.3 / Laravel 12+**.
> Đây không phải bản dịch sách. Nội dung là phần tóm lược tư duy + ví dụ minh hoạ tự soạn để học.

-----

## 1. Chương này nói về cái gì?

Chương 17 là phần “tổng kết” của cuốn sách. Thay vì giảng lý thuyết, Robert C. Martin liệt kê một **danh mục các dấu hiệu code xấu (smells)** và **các quy tắc kinh nghiệm (heuristics)** để nhận biết và sửa chúng.

Cách dùng đúng của chương này:

- Không phải học thuộc lòng. Đây là một **checklist tham chiếu** khi review code và refactor.
- Mỗi smell là một “mùi” – không phải lúc nào cũng sai, nhưng là tín hiệu cần dừng lại và xem xét.
- Các nhóm chính: **Comments (C)**, **Environment (E)**, **Functions (F)**, **General (G)** – nhóm lớn nhất, **Names (N)**, **Tests (T)**. Sách gốc còn có nhóm Java (J); ở đây tôi thay bằng các lưu ý đặc thù **PHP/Laravel**.

Triết lý xuyên suốt: **code phải đọc như văn xuôi, ý định phải rõ ràng, và sự trùng lặp là kẻ thù số một.**

-----

## 2. Comments (Bình luận) – C1 → C5

Nguyên tắc nền: comment tốt là comment giải thích **“tại sao”**, không phải **“cái gì”**. Phần lớn comment là dấu hiệu code chưa đủ rõ.

### C1 – Comment không phù hợp / lỗi thời

Comment chứa thông tin nên nằm ở hệ thống khác (Git, issue tracker). Ví dụ ghi tên tác giả, ngày sửa, số ticket trong code.

```php
// ❌ Thông tin này thuộc về Git, không thuộc về code
// Sửa bởi Nam ngày 2024-03-12, ticket #4521, do bug phân trang
public function paginate(int $perPage): LengthAwarePaginator { /* ... */ }

// ✅ Để Git log lo việc đó
public function paginate(int $perPage): LengthAwarePaginator { /* ... */ }
```

### C2 – Comment thừa (Obsolete / Redundant)

Comment chỉ lặp lại đúng những gì code đã nói. Nó làm loãng, và sớm muộn cũng sai lệch so với code.

```php
// ❌ Comment không thêm thông tin gì
// Lấy user theo id
public function find(int $id): User { return User::findOrFail($id); }

// ✅ Tên hàm đã đủ rõ, bỏ comment
public function find(int $id): User { return User::findOrFail($id); }
```

### C3 – Comment sai (Incorrect)

Comment mô tả một đằng, code làm một nẻo. Đây là loại nguy hiểm nhất vì gây hiểu lầm.

### C4 – Code bị comment lại (Commented-Out Code)

Đừng để code chết nằm trong file. Không ai dám xoá vì sợ “biết đâu cần”. Git đã lưu lịch sử rồi – cứ xoá.

```php
public function total(): int
{
    // ❌ Đống rác ai cũng sợ đụng vào
    // if ($this->isVip) {
    //     $discount = $this->oldDiscount();
    // }
    return $this->subtotal - $this->discount();
}
```

### C5 – Comment đáng lẽ phải là code

Khi bạn cần comment để giải thích một biểu thức, hãy biến lời giải thích đó thành tên biến/hàm.

```php
// ❌
// kiểm tra user đủ tuổi và đã xác thực email
if ($user->age >= 18 && $user->email_verified_at !== null) { /* ... */ }

// ✅ Đưa ý nghĩa vào tên hàm
if ($user->canPlaceOrder()) { /* ... */ }

class User extends Model
{
    public function canPlaceOrder(): bool
    {
        return $this->age >= 18 && $this->hasVerifiedEmail();
    }
}
```

-----

## 3. Environment (Môi trường) – E1 → E2

### E1 – Build phải đơn giản, một bước

Chỉ cần một lệnh để dựng dự án. Người mới vào không nên phải “hỏi anh A để xin file env, hỏi anh B để chạy migration thủ công”.

```bash
# ✅ Mục tiêu: clone xong, một chuỗi lệnh là chạy được
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate --seed
# (hoặc đóng gói vào: composer run setup / Makefile / sail up)
```

### E2 – Test phải chạy bằng một bước

Một lệnh duy nhất chạy toàn bộ test. Không có rào cản nào ngăn lập trình viên chạy test thường xuyên.

```bash
php artisan test
# hoặc: ./vendor/bin/pest
```

-----

## 4. Functions (Hàm) – F1 → F4

### F1 – Quá nhiều tham số

0 tham số là lý tưởng, 1–2 ổn, 3 cần cân nhắc, ≥4 gần như luôn nên gom lại thành object.

```php
// ❌ 6 tham số, dễ truyền nhầm thứ tự
public function createOrder(int $userId, array $items, string $coupon,
    string $address, string $note, bool $isGift): Order { /* ... */ }

// ✅ Gom thành một DTO có ý nghĩa
final class CreateOrderData
{
    public function __construct(
        public readonly int $userId,
        public readonly array $items,
        public readonly ?string $coupon = null,
        public readonly string $address = '',
        public readonly ?string $note = null,
        public readonly bool $isGift = false,
    ) {}
}

public function createOrder(CreateOrderData $data): Order { /* ... */ }
```

### F2 – Tham số đầu ra (Output Arguments)

Hàm không nên sửa tham số truyền vào để “trả kết quả ra ngoài”. Người đọc kỳ vọng tham số là input. Hãy trả về giá trị hoặc dùng method của chính object.

```php
// ❌ appendFooter sửa $report truyền vào
public function appendFooter(Report &$report): void { /* ... */ }

// ✅ Để chính object tự thay đổi trạng thái của nó
$report->appendFooter();
```

### F3 – Cờ điều kiện (Flag Arguments)

Tham số boolean báo hiệu hàm đang làm **hai việc**. Tách thành hai hàm.

```php
// ❌
public function render(bool $isAdmin): string { /* ... */ }

// ✅
public function renderForAdmin(): string { /* ... */ }
public function renderForGuest(): string { /* ... */ }
```

### F4 – Hàm chết (Dead Function)

Phương thức không ai gọi thì xoá đi. IDE/Git cho bạn tìm lại nếu cần.

-----

## 5. General (Tổng quát) – G1 → G36

Đây là phần dài và quan trọng nhất. Dưới đây nhóm lại theo chủ đề cho dễ nhớ.

### Nhóm: Trùng lặp & một-nguồn-sự-thật

**G5 – Trùng lặp (Duplication).** “Don’t Repeat Yourself”. Đây là smell hàng đầu. Mọi đoạn lặp đều là cơ hội trừu tượng hoá bị bỏ lỡ.

```php
// ❌ Logic tính giá sau giảm lặp ở 3 nơi
$priceA = $a->price - ($a->price * 0.1);
$priceB = $b->price - ($b->price * 0.1);

// ✅ Một nguồn sự thật
final class Discount
{
    public static function apply(int $price, float $rate = 0.1): int
    {
        return (int) round($price - $price * $rate);
    }
}
```

**G6 – Code ở sai mức trừu tượng.** Khái niệm cấp cao và chi tiết cấp thấp không nên trộn trong cùng một class/hàm.

**G10 – Dọc kề nhau theo logic (Vertical Separation).** Biến và hàm nên được khai báo gần nơi sử dụng. Hàm private nên nằm ngay dưới hàm gọi nó.

### Nhóm: Ý định rõ ràng

**G16 – Ý định bị che mờ (Obscured Intent).** Code “thông minh” quá mức làm khó đọc. Ưu tiên rõ ràng hơn ngắn gọn.

```php
// ❌ Khó đọc
return $d * 8 * 60 + $h * 60 + $m;

// ✅ Rõ ý định
$workHoursPerDay = 8;
return ($days * $workHoursPerDay + $hours) * 60 + $minutes; // tổng số phút
```

**G19 – Dùng biến giải thích (Explaining Variable).** Tách biểu thức phức tạp ra biến có tên.

```php
// ✅
$isWeekend = in_array($date->dayOfWeek, [Carbon::SATURDAY, Carbon::SUNDAY], true);
$isBusinessHour = $date->hour >= 9 && $date->hour < 18;

if (! $isWeekend && $isBusinessHour) { /* ... */ }
```

**G20 – Tên hàm phải nói lên việc nó làm.** Nếu phải đọc thân hàm mới biết nó làm gì thì tên đã thất bại.

**G21 – Hiểu thuật toán.** Đừng “code cho đến khi test pass”. Phải thật sự hiểu vì sao nó đúng.

### Nhóm: Hành vi đúng & nhất quán

**G1 – Nhiều ngôn ngữ trong một file.** Tránh trộn PHP + HTML + SQL + JS lộn xộn trong một file. Blade tách view, query builder tách SQL.

**G2 – Hành vi hiển nhiên không được cài đặt (Principle of Least Surprise).** Hàm nên làm điều người ta kỳ vọng. `Carbon::parse('xx')` nên xử lý các định dạng phổ biến.

**G3 – Hành vi biên không đúng (Incorrect Boundary Behavior).** Đừng tin vào trực giác về các trường hợp biên. Hãy viết test cho chúng (rỗng, null, 0, âm, vượt giới hạn).

**G4 – Bỏ qua phòng vệ an toàn (Overridden Safeties).** Đừng tắt cảnh báo, đừng `@` chặn lỗi PHP, đừng bỏ qua test đang fail.

```php
// ❌ Nuốt lỗi
$data = @json_decode($raw);

// ✅ Xử lý tường minh
$data = json_decode($raw, true, flags: JSON_THROW_ON_ERROR);
```

**G23 – Ưu tiên đa hình hơn if/else và switch.** Chuỗi switch theo “loại” thường nên thay bằng đa hình.

```php
// ❌ switch theo type lặp đi lặp lại nhiều nơi
function fee(string $type): int {
    return match ($type) {
        'standard' => 0,
        'express'  => 50000,
        'overnight'=> 120000,
    };
}

// ✅ Đa hình
interface ShippingMethod { public function fee(): int; }

final class Standard  implements ShippingMethod { public function fee(): int { return 0; } }
final class Express   implements ShippingMethod { public function fee(): int { return 50_000; } }
final class Overnight implements ShippingMethod { public function fee(): int { return 120_000; } }
```

**G25 – Thay số “ma thuật” bằng hằng số có tên.**

```php
// ❌
if ($order->total > 500000) { /* freeship */ }

// ✅
private const FREE_SHIPPING_THRESHOLD = 500_000;
if ($order->total > self::FREE_SHIPPING_THRESHOLD) { /* freeship */ }
```

**G28 – Đóng gói điều kiện.** Biểu thức boolean phức tạp nên gói vào hàm có tên (xem lại C5/G19).

**G30 – Hàm chỉ nên làm một việc.** Nếu mô tả hàm phải dùng chữ “và”, hãy tách.

**G31 – Liên kết thời gian ẩn (Hidden Temporal Coupling).** Nếu các bước phải gọi đúng thứ tự, hãy thiết kế API ép buộc thứ tự đó (ví dụ bước sau nhận output của bước trước làm tham số).

**G34 – Hàm không nên đi sâu quá một cấp trừu tượng.** Thân hàm nên ở cùng một “tầng”.

### Nhóm: Phụ thuộc & ranh giới

**G7 – Class cha phụ thuộc class con.** Lớp cơ sở không được biết về lớp dẫn xuất.

**G8 – Quá nhiều thông tin (giao diện hẹp).** Class/interface nên phơi bày càng ít càng tốt. Đóng gói chặt.

**G13 – Liên kết giả tạo (Artificial Coupling).** Đừng đặt thứ không liên quan cạnh nhau chỉ vì tiện.

**G14 – Ghen tị tính năng (Feature Envy).** Method dùng dữ liệu của class khác nhiều hơn của chính nó → có lẽ nên chuyển method sang class kia.

```php
// ❌ OrderService "ghen tị" dữ liệu của Order
$total = $order->subtotal + $order->tax - $order->discount;

// ✅ Để Order tự tính
class Order extends Model
{
    public function total(): int
    {
        return $this->subtotal + $this->tax - $this->discount;
    }
}
```

**G17 – Trách nhiệm đặt sai chỗ.** Code nên nằm nơi người đọc kỳ vọng tìm thấy nó.

**G18 – Static không phù hợp.** Chỉ dùng static khi chắc chắn không bao giờ cần đa hình. Static khó test/mock.

### Nhóm: Cấu trúc & quy ước

**G11 – Không nhất quán.** Làm một việc giống nhau theo cùng một cách ở mọi nơi (đặt tên, cấu trúc, format).

**G12 – Rác (Clutter).** Constructor rỗng, biến không dùng, hàm vô nghĩa – xoá hết.

**G15 – Toán tử selector (chuỗi if/switch chọn nhánh ngay tại lời gọi).** Truyền cờ để chọn hành vi là dấu hiệu nên tách hàm (liên hệ F3).

**G24 – Tuân theo quy ước chuẩn.** PHP có PSR-12, Laravel có quy ước riêng (tên migration, resource controller…). Theo nhóm, đừng theo ý thích cá nhân.

**G26 – Chính xác.** Đừng đoán. Tiền dùng kiểu nguyên (xu) hoặc thư viện money; xử lý null tường minh; lường trước truy vấn trả về rỗng.

**G27 – Cấu trúc hơn quy ước.** Ép buộc thiết kế bằng cấu trúc (kiểu, enum, interface) thay vì chỉ dựa vào quy ước đặt tên.

```php
// ✅ Enum ép buộc tập giá trị hợp lệ, không cần "quy ước string"
enum OrderStatus: string
{
    case Pending   = 'pending';
    case Paid      = 'paid';
    case Shipped   = 'shipped';
    case Cancelled = 'cancelled';
}
```

**G29 – Tránh điều kiện phủ định.** `if ($buffer->shouldCompact())` dễ đọc hơn `if (! $buffer->shouldNotCompact())`.

**G32 – Code tuỳ tiện, thiếu cấu trúc.** Có lý do cho mọi cách tổ chức; nếu tuỳ tiện, người sau sẽ bắt chước cái tuỳ tiện đó.

**G33 – Đóng gói điều kiện biên.** Tính toán biên (ví dụ `$level + 1`) làm một lần, đặt vào biến có tên.

```php
// ✅
$nextLevel = $level + 1;
$tags[$nextLevel] = ...;
if ($nextLevel < self::MAX) { /* dùng $nextLevel tiếp */ }
```

**G35 – Dữ liệu cấu hình nên ở mức cao.** Hằng số cấu hình nên truyền từ trên xuống (config/env), không chôn sâu trong hàm cấp thấp.

```php
// ✅ Laravel: đọc từ config thay vì hardcode trong service
$threshold = config('shipping.free_threshold');
```

**G36 – Tránh điều hướng bắc cầu (Law of Demeter / Train Wreck).** Mỗi module chỉ nên biết “hàng xóm” trực tiếp.

```php
// ❌ Train wreck — biết quá sâu cấu trúc nội bộ
$city = $order->getCustomer()->getAddress()->getCity()->getName();

// ✅ Hỏi cái mình cần, để object trung gian lo phần còn lại
$city = $order->customerCityName();
```

**G9 – Code chết (Dead Code).** Nhánh if không bao giờ chạy, hàm không ai gọi, `catch` không bao giờ xảy ra → xoá.

**G22 – Logic làm rõ ràng hoá những thứ ngầm định.** Những phụ thuộc/giả định cần được nêu rõ trong code.

-----

## 6. Names (Đặt tên) – N1 → N7

### N1 – Dùng tên mô tả

Tên là tài liệu sống. Đặt tên kỹ, đổi tên không ngại khi hiểu rõ hơn.

```php
// ❌
$d = now()->diffInDays($u->created_at);

// ✅
$daysSinceRegistration = now()->diffInDays($user->created_at);
```

### N2 – Tên phù hợp mức trừu tượng

Tên phản ánh “cái gì”, không phản ánh “cách cài đặt”.

```php
// ❌ tên lộ chi tiết cài đặt
interface ModemConnectionViaUsbCable { /* ... */ }
// ✅
interface Modem { /* ... */ }
```

### N3 – Dùng từ vựng chuẩn khi có thể

Theo thuật ngữ kỹ thuật quen thuộc (Repository, Factory, Observer) hoặc thuật ngữ nghiệp vụ. Đừng tự chế từ lạ cho khái niệm đã có tên.

### N4 – Tên rõ nghĩa, không mơ hồ

Tránh `data`, `info`, `manager`, `process`, `do`, `temp` khi chúng không nói gì.

### N5 – Tên dài cho phạm vi rộng

Biến vòng lặp `$i` chấp nhận được. Nhưng property/class sống lâu và dùng rộng thì cần tên dài, rõ.

### N6 – Tránh mã hoá kiểu trong tên

Không Hungarian notation, không tiền tố `m_`, không nhồi kiểu vào tên. PHP đã có type hint.

```php
// ❌
private string $strName;
private array $arrItems;
// ✅
private string $name;
private array $items;
```

### N7 – Tên nên mô tả tác dụng phụ

Hàm có side-effect nên thể hiện điều đó trong tên.

```php
// ❌ "get" nhưng lại tạo mới nếu chưa có
public function getOrCreateCart(): Cart { /* ... */ }  // tạm chấp nhận vì tên đã nói rõ
// ❌ thực sự tệ: tên nói "get" nhưng âm thầm tạo
public function getCart(): Cart { /* nếu null thì tạo + lưu DB */ }
```

-----

## 7. Tests – T1 → T9

### T1 – Test không đủ

Test phải phủ mọi thứ *có thể hỏng*. Còn điều kiện chưa được kiểm tra nghĩa là test chưa đủ.

### T2 – Dùng công cụ đo coverage

Dùng coverage để thấy phần code chưa được test.

```bash
php artisan test --coverage --min=80
```

### T3 – Đừng bỏ qua test nhỏ/dễ

Test “tầm thường” vẫn có giá trị làm tài liệu.

### T4 – Test bị bỏ (skipped) là một câu hỏi

Test `markTestSkipped` treo lơ lửng là dấu hiệu một yêu cầu chưa rõ – cần xử lý dứt điểm, không để mãi.

### T5 – Test điều kiện biên

Trung tâm thường đúng; lỗi nằm ở biên (rỗng, 1 phần tử, max, âm, null).

```php
it('tính freeship đúng tại đúng ngưỡng', function () {
    expect(Shipping::isFree(499_999))->toBeFalse();
    expect(Shipping::isFree(500_000))->toBeTrue();   // đúng ngay tại biên
    expect(Shipping::isFree(0))->toBeFalse();
});
```

### T6 – Kiểm tra kỹ quanh chỗ vừa có bug

Bug thường đi theo cụm. Sửa bug xong, test thật kỹ vùng lân cận.

### T7 – Mẫu thất bại tiết lộ nguyên nhân

Sắp xếp test có hệ thống để khi một số test fail, *cách chúng fail* chỉ ra nguyên nhân.

### T8 – Mẫu coverage tiết lộ nguyên nhân

Xem dòng nào *không* được test khi fail cũng cho manh mối.

### T9 – Test phải nhanh

Test chậm sẽ không được chạy thường xuyên. Tách integration ra khỏi unit; dùng database in-memory cho test.

```php
// phpunit.xml: dùng sqlite :memory: cho tốc độ
// <env name="DB_CONNECTION" value="sqlite"/>
// <env name="DB_DATABASE" value=":memory:"/>
```

Nguyên tắc gộp cho test sạch: **F.I.R.S.T** – Fast, Independent, Repeatable, Self-validating, Timely.

-----

## 8. Lưu ý đặc thù PHP / Laravel 12 (thay cho mục Java trong sách)

Sách gốc có nhóm J (Java). Dưới đây là phiên bản tương đương cho hệ sinh thái PHP/Laravel:

- **Theo PSR-12 / PER Coding Style.** Dùng Laravel Pint (`./vendor/bin/pint`) để tự động hoá, không tranh cãi format thủ công.
- **Dùng kiểu chặt.** Khai báo `declare(strict_types=1);`, type hint đầy đủ tham số và giá trị trả về, `readonly` cho DTO/Value Object.
- **Tránh Facade và helper toàn cục trong tầng domain.** Chúng giống static (G18) – khó test. Inject dependency qua constructor.
- **Eloquent: cẩn thận N+1 (một dạng của G5/G26).** Dùng eager loading `with()`, bật `Model::preventLazyLoading()` ở môi trường dev.
- **Fat controller là smell.** Controller chỉ điều phối. Logic nghiệp vụ đẩy vào Action / Service; truy vấn vào Query/Repository; validate vào Form Request.
- **Đừng để query trong Blade** (vi phạm G1 + G6). View chỉ trình bày dữ liệu đã chuẩn bị sẵn.
- **Dùng Enum thay magic string** cho status/type (G25, G27).
- **config() ở tầng cao, không env() rải rác.** Chỉ gọi `env()` trong file config; phần còn lại dùng `config()` (liên hệ G35).

```php
<?php
declare(strict_types=1);

// ✅ Controller mỏng, đẩy việc cho Action — gom nhiều heuristic
final class CheckoutController
{
    public function __construct(private readonly PlaceOrder $placeOrder) {}

    public function store(PlaceOrderRequest $request): JsonResponse
    {
        $order = $this->placeOrder->execute(
            CreateOrderData::fromRequest($request)
        );

        return OrderResource::make($order)->response();
    }
}
```

-----

## 9. Checklist nhanh khi review code

In phần này ra dùng khi đọc Pull Request:

- [ ] Có đoạn nào lặp lại không? (G5)
- [ ] Comment nào chỉ lặp lại code, hoặc là code bị comment? Xoá. (C2, C4)
- [ ] Hàm có làm đúng *một* việc không? Tên có nói đúng việc đó không? (G30, N1)
- [ ] Có tham số cờ boolean / quá 3 tham số không? (F1, F3)
- [ ] Có số/chuỗi ma thuật nào nên thành hằng/Enum không? (G25, G27)
- [ ] Có chuỗi switch theo “type” nên chuyển đa hình không? (G23)
- [ ] Điều kiện biên đã có test chưa? (G3, T5)
- [ ] Có chuỗi gọi `->a()->b()->c()->d()` (train wreck) không? (G36)
- [ ] Logic nghiệp vụ có lọt vào controller/Blade không? (G1, G17)
- [ ] Test có chạy nhanh và độc lập không? (T9, FIRST)

-----

## 10. Cách áp dụng để hình thành tư duy

1. **Chọn 1 smell mỗi tuần.** Đừng cố nhớ hết. Tuần này chỉ soi G5 (trùng lặp) trong code mình viết.
1. **Refactor có test bảo vệ.** Mọi thay đổi phải có test xanh trước và sau – đây là tinh thần cốt lõi của Clean Code.
1. **Đặt tên là thao tác refactor.** Mỗi lần đọc lại thấy tên chưa rõ, đổi ngay (N1).
1. **Boy Scout Rule.** Mỗi lần đụng vào file, để nó sạch hơn một chút so với lúc bạn mở ra.
1. **Đọc lại chương này như checklist**, không phải như sách – nó được thiết kế để tra cứu khi làm việc thật.

-----

*Tài liệu học tập tự soạn. Để học chính xác và đầy đủ, bạn nên đọc trực tiếp cuốn “Clean Code” (Robert C. Martin), chương 17.*