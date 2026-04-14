Trong Chương 7 của cuốn sách "Clean Code", tác giả Michael Feathers trình bày khái niệm **"Define the Normal Flow"** (Xác định luồng xử lý bình thường) nhằm giúp lập trình viên tách biệt logic nghiệp vụ khỏi logic xử lý lỗi, giúp mã nguồn trở nên sạch sẽ và dễ đọc hơn [1, 2].

### 1. Phân tích triết lý "Normal Flow"
Thông thường, khi áp dụng các kỹ thuật xử lý ngoại lệ, chúng ta có xu hướng đẩy việc phát hiện lỗi ra các biên của chương trình [3]. Tuy nhiên, đôi khi việc sử dụng `try-catch` để xử lý các trường hợp đặc biệt lại làm gián đoạn luồng suy nghĩ chính của thuật toán, khiến mã nguồn bị lộn xộn [4].

Mục tiêu của "Normal Flow" là đưa mã nguồn về trạng thái một **thuật toán thuần túy và đơn giản**, nơi người đọc không bị phân tâm bởi các khối xử lý ngoại lệ xen kẽ [3, 4]. Để đạt được điều này, tác giả đề xuất sử dụng **Mẫu đối tượng đặc biệt (Special Case Pattern)** [5]. Thay vì bắt một ngoại lệ để xử lý trường hợp không bình thường, bạn trả về một đối tượng có hành vi phù hợp với trường hợp đó một cách âm thầm [5].

### 2. Ví dụ thực tế với PHP

Hãy tưởng tượng bạn đang viết một hệ thống tính chi phí công tác, trong đó có quy định: nếu nhân viên không có hóa đơn ăn uống, họ sẽ được hưởng mức phụ cấp cố định hàng ngày (per diem) [4].

#### Cách làm chưa tốt (Sử dụng Exception để điều hướng logic):
Ở đây, việc thiếu hóa đơn được coi là một "lỗi" và xử lý trong khối `catch`, điều này làm luồng xử lý bị ngắt quãng [4, 6].

```php
try {
    $expenses = $expenseReportDAO->getMeals($employee->id);
    $total += $expenses->getTotal();
} catch (MealExpensesNotFound $e) {
    // Luồng chính bị ngắt quãng bởi xử lý ngoại lệ
    $total += $this->getMealPerDiem();
}
```

#### Cách làm sạch (Áp dụng Special Case Pattern):
Chúng ta sẽ tạo ra một đối tượng đặc biệt để xử lý trường hợp "không có hóa đơn" ngay từ tầng dữ liệu (DAO). Khi đó, luồng xử lý chính ở tầng nghiệp vụ sẽ cực kỳ đơn giản và không có ngoại lệ nào bị tung ra [5, 6].

```php
// Tầng nghiệp vụ: Luồng xử lý bình thường (Normal Flow)
// Mã nguồn trông như một thuật toán thuần túy, không có try-catch [3]
$expenses = $expenseReportDAO->getMeals($employee->id);
$total += $expenses->getTotal(); 

// --- Cấu trúc phía sau để hỗ trợ Normal Flow ---

interface MealExpenses {
    public function getTotal(): int;
}

class RealMealExpenses implements MealExpenses {
    public function getTotal(): int {
        // Trả về tổng tiền trên hóa đơn thực tế
        return $this->sumOfReceipts;
    }
}

// Đối tượng đặc biệt (Special Case Object) [5]
class PerDiemMealExpenses implements MealExpenses {
    public function getTotal(): int {
        // Trả về mức phụ cấp mặc định thay vì tung ra lỗi [6]
        return 500000; // 500k VNĐ/ngày
    }
}
```

### 3. Lợi ích của cách tiếp cận này
*   **Mã nguồn sạch hơn:** Luồng logic chính nhìn rất sáng sủa, chỉ tập trung vào việc cộng tổng chi phí [6].
*   **Dễ bảo trì:** Bạn không phải kiểm tra `null` hoặc bắt ngoại lệ ở khắp mọi nơi trong ứng dụng [5, 7].
*   **Tính ổn định:** Tránh được các lỗi bất ngờ như `NullPointerException` (trong PHP là lỗi gọi phương thức trên null) vì luôn có một đối tượng hợp lệ được trả về [7, 8].

Việc coi xử lý lỗi là một **mối quan tâm riêng biệt** và giữ cho luồng chính không bị "ô nhiễm" bởi logic xử lý sai sót là chìa khóa để tạo ra mã nguồn mạnh mẽ và bền vững [9].