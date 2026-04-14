# Tổng hợp nội dung cần nắm: Đừng trả về null / Đừng truyền null vào hàm

Dưới đây là phần **tổng hợp nội dung cần nắm** về hai ý trong *Clean Code – Chương 7 (Error Handling)*:

- **Đừng trả về `null`**
- **Đừng truyền `null` vào hàm**

---

## 1. Vì sao `null` là vấn đề?

`null` nhìn thì đơn giản, nhưng thường làm code:

- khó đoán hơn
- buộc nơi gọi phải kiểm tra liên tục
- dễ sinh lỗi runtime
- che giấu thiết kế chưa rõ ràng
- làm trách nhiệm giữa các hàm bị mập mờ

Nói ngắn gọn: `null` thường đẩy gánh nặng xử lý lỗi sang chỗ khác.

---

## 2. Đừng trả về `null`

### Ý chính
Một hàm trả về `null` buộc code gọi phải luôn nhớ kiểm tra. Chỉ cần quên một chỗ là dễ phát sinh lỗi.

Ví dụ chưa tốt:

```php
public function findUserByEmail(string $email): ?User
{
    return null;
}
```

Code gọi:

```php
$user = $service->findUserByEmail($email);
echo $user->name;
```

Nếu quên check `null`, lỗi sẽ xuất hiện ở nơi sử dụng, không phải nơi phát sinh vấn đề.

---

## 3. Nên thay `null` bằng gì?

Điều này phụ thuộc vào ý nghĩa nghiệp vụ.

### Cách 1: Throw exception
Dùng khi trường hợp đó là **bất thường** và không nên tiếp tục luồng xử lý.

```php
public function getUserByEmail(string $email): User
{
    $user = $this->repository->findByEmail($email);

    if ($user === null) {
        throw new UserNotFoundException($email);
    }

    return $user;
}
```

Phù hợp khi hệ thống kỳ vọng dữ liệu phải tồn tại.

---

### Cách 2: Trả về collection rỗng
Dùng khi “không có dữ liệu” là trạng thái bình thường.

```php
public function getActiveOrders(): array
{
    return [];
}
```

Tốt hơn nhiều so với:

```php
public function getActiveOrders(): ?array
{
    return null;
}
```

Vì code gọi sẽ đơn giản hơn:

```php
foreach ($service->getActiveOrders() as $order) {
    // xử lý
}
```

---

### Cách 3: Dùng Null Object
Dùng khi muốn tránh `if ($x === null)` lặp đi lặp lại.

```php
interface Customer
{
    public function getDisplayName(): string;
}

final class RealCustomer implements Customer
{
    public function __construct(private string $name) {}

    public function getDisplayName(): string
    {
        return $this->name;
    }
}

final class GuestCustomer implements Customer
{
    public function getDisplayName(): string
    {
        return 'Guest';
    }
}
```

Thay vì trả `null`, trả `GuestCustomer`.

---

### Cách 4: Tách rõ “tìm” và “lấy”
Đây là cách rất thực tế trong PHP.

- `find...()` có thể chấp nhận không tìm thấy
- `get...()` nên trả dữ liệu hợp lệ hoặc throw exception

Ví dụ:

```php
public function findUserById(int $id): ?User
{
    // có thể không tìm thấy
}

public function getUserById(int $id): User
{
    $user = $this->findUserById($id);

    if ($user === null) {
        throw new UserNotFoundException((string) $id);
    }

    return $user;
}
```

Cách này làm API rõ nghĩa hơn.

---

## 4. Đừng truyền `null` vào hàm

### Ý chính
Nếu một hàm nhận `null`, điều đó thường cho thấy:

- input chưa được kiểm tra từ trước
- contract của hàm không rõ
- hàm đang phải gánh quá nhiều trường hợp
- luồng nghiệp vụ bị trộn lẫn

Ví dụ chưa tốt:

```php
public function sendEmail(?string $email): void
{
    if ($email === null) {
        return;
    }

    // send email
}
```

Hàm này âm thầm bỏ qua lỗi thay vì nói rõ có vấn đề.

---

## 5. Khi nào không nên truyền `null`?

Không nên truyền `null` khi:

- tham số đó là bắt buộc
- `null` chỉ là cách “né lỗi”
- hàm không có ý nghĩa rõ ràng khi nhận `null`

Tốt hơn là:

```php
public function sendEmail(string $email): void
{
    // send email
}
```

Và kiểm tra dữ liệu trước khi gọi hàm.

---

## 6. Nếu thật sự có hai trường hợp khác nhau, hãy tách hàm

Thay vì:

```php
public function createUser(?string $email): void
{
    if ($email === null) {
        // xử lý kiểu khác
    }
}
```

Hãy tách rõ ý định:

```php
public function createUserWithEmail(string $email): void
{
    // ...
}

public function createGuestUser(): void
{
    // ...
}
```

Cách này giúp tên hàm thể hiện đúng nghiệp vụ.

---

## 7. Khi nào `null` có thể chấp nhận được?

*Clean Code* không nói `null` là tuyệt đối cấm, mà nói nên **tránh tối đa**.

`null` có thể chấp nhận khi:

- đó thật sự là một phần của domain
- ý nghĩa của `null` rõ ràng, không mơ hồ
- nơi nhận biết chắc chắn phải xử lý nó

Ví dụ:

- `middle_name` có thể không có
- `deleted_at` có thể là `null` nếu chưa xóa
- bộ lọc tìm kiếm tùy chọn có thể vắng mặt

Nhưng ngay cả khi đó, vẫn nên cân nhắc kỹ xem có cách biểu đạt rõ hơn không.

---

## 8. Dấu hiệu code đang lạm dụng `null`

Bạn nên xem lại thiết kế nếu thấy các dấu hiệu này:

- rất nhiều kiểu `?string`, `?array`, `?User`
- hàm nào cũng có `if ($x === null)`
- controller/service đầy kiểm tra `null`
- bug kiểu “call on null” xuất hiện thường xuyên
- cùng một giá trị `null` nhưng mỗi nơi hiểu một kiểu khác nhau

---

## 9. Nguyên tắc thực tế để áp dụng trong dự án PHP

### Với giá trị trả về
- Không trả `null` nếu có thể trả về object hợp lệ, collection rỗng, hoặc throw exception.
- Phân biệt rõ hàm “tìm” và hàm “lấy”.
- Nếu không có dữ liệu là bình thường, trả về rỗng.
- Nếu không có dữ liệu là bất thường, throw exception.

### Với tham số đầu vào
- Không cho phép `null` nếu hàm cần dữ liệu bắt buộc.
- Validate trước khi gọi hàm.
- Nếu `null` dẫn đến một luồng nghiệp vụ khác, hãy tách thành hàm khác.
- Dùng type hint rõ ràng để ép contract.

---

## 10. Tinh thần cốt lõi cần nhớ

Hai ý này thực chất xoay quanh một nguyên tắc lớn hơn:

**Hãy làm cho contract của hàm rõ ràng.**

Người đọc hàm cần hiểu ngay:

- hàm này có luôn trả về giá trị hợp lệ không
- khi lỗi thì nó làm gì
- nó có chấp nhận input thiếu hay không
- “không có dữ liệu” là trạng thái bình thường hay là lỗi

Nếu dùng `null` quá nhiều, câu trả lời cho các câu hỏi trên sẽ trở nên mơ hồ.

---

## 11. Một bản tóm tắt rất ngắn

- **Đừng trả về `null`** vì bắt người gọi phải tự phòng thủ và dễ quên check.
- **Đừng truyền `null` vào hàm** nếu `null` không phải giá trị hợp lệ thật sự.
- Thay thế bằng:
  - exception
  - collection rỗng
  - default object / Null Object
  - tách hàm để biểu đạt rõ nghiệp vụ
- Mục tiêu cuối cùng là làm code **rõ nghĩa, ít phòng thủ thừa, ít bug hơn**.
