# Clean Code - Chương 10

## 1. Nội dung cốt lõi của chương

### 1.1 Tổ chức class (Class Organization)

#### a. Tính đóng gói

Tính đóng gói nghĩa là class nên che giấu chi tiết triển khai bên trong và chỉ để lộ ra bên ngoài những hành vi thật sự cần thiết.

Điều này giúp class kiểm soát được dữ liệu nội bộ và tránh việc các class khác phụ thuộc vào chi tiết triển khai.

Trong PHP/Laravel, điều này thường có nghĩa là:

- Property nên ưu tiên `private`
- Helper method nội bộ nên ưu tiên `private`
- Chỉ dùng `public` cho những hành vi mà bên ngoài class thật sự cần gọi
- Chỉ dùng `protected` khi class con thật sự cần mở rộng hành vi đó
- Không nên đổi `private` thành `protected` chỉ để unit test dễ hơn

Ví dụ:

Bad

```php
namespace App\Services;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

class DocumentUploadService
{
    public function upload(UploadedFile $file): string
    {
        $this->validateFile($file);

        $path = $this->buildStoragePath($file);

        Storage::disk('local')->put($path, $file->getContent());

        return $path;
    }

    protected function validateFile(UploadedFile $file): void
    {
        // Validation logic
    }

    protected function buildStoragePath(UploadedFile $file): string
    {
        // Build storage path logic
    }
}
```

Vấn đề của ví dụ trên:

- `validateFile` và `buildStoragePath` là các helper method nội bộ, không cần thiết phải để `protected`.
- Việc để `protected` có thể khiến các class con vô tình phụ thuộc vào chi tiết triển khai của `DocumentUploadService`, khiến việc refactor sau này trở nên khó khăn hơn.

Good

```php
namespace App\Services;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

class DocumentUploadService
{
    public function upload(UploadedFile $file): string
    {
        $this->validateFile($file);

        $path = $this->buildStoragePath($file);

        Storage::disk('local')->put($path, $file->getContent());

        return $path;
    }

    private function validateFile(UploadedFile $file): void
    {
        if (! in_array($file->extension(), ['pdf', 'docx', 'txt'], true)) {
            throw new \InvalidArgumentException('Unsupported file type.');
        }

        if ($file->getSize() > 10 * 1024 * 1024) {
            throw new \InvalidArgumentException('File size must not exceed 10MB.');
        }
    }

    private function buildStoragePath(UploadedFile $file): string
    {
        return sprintf(
            'documents/%s/%s.%s',
            now()->format('Y/m/d'),
            str()->uuid(),
            $file->extension()
        );
    }
}
```
Ở phiên bản này:

- `validateFile` và `buildStoragePath` đã được đổi thành `private`, giúp bảo vệ chi tiết triển khai của `DocumentUploadService`.
- Điều này giúp class dễ dàng refactor sau này mà không lo bị ảnh hưởng đến các class con hoặc các phần khác của codebase.

**Không nên đổi `private` thành `protected` chỉ để unit test dễ hơn.**

Giả sử hệ thống cần test DocumentUploadService, để có thể test được `validateFile` team đã đổi chúng thành `protected` để có thể tạo một class con trong test và gọi được các method này. Đây là một sai lầm phổ biến.

```php
class DocumentUploadService
{
    public function upload(UploadedFile $file): string
    {
        $this->validateFile($file);

        // upload logic
    }

    protected function validateFile(UploadedFile $file): void
    {
        // validation logic
    }
}

class TestableDocumentUploadService extends DocumentUploadService
{
    public function callValidateFile(UploadedFile $file): void
    {
        $this->validateFile($file);
    }
}

```

Cách này không nên là lựa chọn đầu tiên, vì ta đang làm yếu đi tính đóng gói chỉ để phục vụ kiểm thử.

Thay vào đó, nên test thông qua hành vi public của class:

```php

it('rejects unsupported file type', function () {
    $service = new DocumentUploadService();

    $file = UploadedFile::fake()->create('malware.exe', 100);

    expect(fn () => $service->upload($file))
        ->toThrow(InvalidArgumentException::class, 'Unsupported file type.');
});
```

**Khi nào có thể tách private method thành class riêng?**

Nguyên tắc: Nếu một private method trở nên phức tạp, có nhiều rule, hoặc cần test độc lập, thay vì đổi nó thành protected, nên cân nhắc tách nó thành một class riêng.

Ví dụ, nếu `validateFile` trở nên phức tạp với nhiều rule, có thể tách nó thành một class mới:

```php
class DocumentFileValidator
{
    public function validate(UploadedFile $file): void
    {
        if (! in_array($file->extension(), ['pdf', 'docx', 'txt'], true)) {
            throw new \InvalidArgumentException('Unsupported file type.');
        }
        if ($file->getSize() > 10 * 1024 * 1024) {
            throw new \InvalidArgumentException('File size must not exceed 10MB.');
        }
    }
}
```

Sau đó `DocumentUploadService` sẽ sử dụng `FileValidator`:

```php
class DocumentUploadService
{
    private DocumentFileValidator $validator;

    public __construct(DocumentFileValidator $fileValidator)
    {
        $this->validator = $fileValidator;
    }

    public function upload(UploadedFile $file): string
    {
        $this->validator->validate($file);

        // upload logic
    }
}
```

Lúc này `DocumentFileValidator` có thể được test độc lập thông qua method public là `validate`. Đây là một cách tiếp cận tốt hơn so với việc đổi private method thành protected chỉ để test.

```php
it('file correctly', function () {
    $validator = new DocumentFileValidator();

    $validFile = $file = UploadedFile::fake()->create('malware.exe', 100);
    expect(fn () => $validator->validate($validFile))->not()->toThrow();
});

it('rejects unsupported file type', function () {
    $validator = new DocumentFileValidator();

    $invalidFile = UploadedFile::fake()->create('malware.exe', 100);

    expect(fn () => $validator->validate($invalidFile))
        ->toThrow(InvalidArgumentException::class, 'Unsupported file type.');
});
```

#### b. Nguyên tắc tổ chức

Một class nên được tổ chức theo một quy tắc nhất định để dễ đọc và bảo trì.

Trong PHP, PER Coding Style là các chuẩn coding style phổ biến và úy tín.

Các quy tắc tổ chức class bao gồm:

1. Namespace
2. Use statements
3. Class declaration
4. Constants
5. Properties
6. Constructor
7. Public methods
8. Protected methods
9. Private methods

Ví dụ

```php
<?php
// 1. Namespace
namespace App\Services;

// 2. Use statements
use App\Models\User;
use App\Data\UserData;

// 3. Class declaration
class UserService {
    // 4. Constants
    const DEFAULT_STATUS = 'active';

    // 5. Properties
    private UserRepositoryInterface $userRepository;

    // 6. Constructor
    public function __construct(UserRepositoryInterface $userRepository) {
        $this->userRepository = $userRepository;
    }

    // 7. Public method
    public function create(UserData $data): User {
        if (!$this->validateData($data)) {
            throw new InvalidArgumentException('Invalid user data');
        }

        $this->userRepository->save(new UserData($data));

        $this->log('User created: ' . $data->email);

        return $user;
    }

    // 8. Protected method
    protected function validateData(array $data): bool {
        return isset($data['email']) && filter_var($data['email'], FILTER_VALIDATE_EMAIL);
    }

    // 9. Private method
    private function log(string $message): void {
        // Log user creation
    }
}

```

#### c. Công cụ hỗ trợ

- Các IDE hiện đại như PhpStorm, Visual Studio Code có thể tự động sắp xếp code theo chuẩn PER Coding Style.
- Với các framework như Laravel, Symfony, có thể sử dụng các package như PHP CS Fixer để tự động format code theo chuẩn.

Cấu hình PHP CS Fixer

```php
<?php

use PhpCsFixer\Config;
use PhpCsFixer\Finder;

$finder = Finder::create()
    ->in(__DIR__ . '/app')
    ->name('*.php');

return (new Config())
    ->setRules([
        '@PSR12' => true,

        'ordered_imports' => [
            'sort_algorithm' => 'alpha',
        ],

        'ordered_class_elements' => [
            'order' => [
                'use_trait',

                'case',

                'constant_public',
                'constant_protected',
                'constant_private',

                'property_public',
                'property_protected',
                'property_private',

                'construct',

                'method_public',
                'method_protected',
                'method_private',
            ],
        ],
    ])
    ->setFinder($finder);
```

Run PHP CS Fixer

```bash
vendor/bin/php-cs-fixer fix
```

### 1.2 Các lớp nên được làm nhỏ

#### a. Tại sao cần làm nhỏ class?

Nếu một class có quá nhiều trách nhiệm, quá nhiều method, nó sẽ trở nên khó hiểu, khó sửa, và khó test.
Lúc này nó sẽ được gọi là “God Class”.

Một God Class thường gây ra các vấn đề sau:

| Vấn đề                   | Hậu quả                                         |
| ------------------------ | ----------------------------------------------- |
| Quá nhiều trách nhiệm    | Khó hiểu class thật sự làm gì                   |
| Quá nhiều method         | Dev khó tìm đúng nơi cần sửa                    |
| Quá nhiều dependency     | Constructor phình to, khó test                  |
| Nhiều nơi cùng phụ thuộc | Sửa một chỗ dễ ảnh hưởng dây chuyền             |
| Khó viết unit test       | Test phải setup quá nhiều dependency            |
| Khó review code          | Reviewer khó đánh giá thay đổi có an toàn không |
| Dễ phát sinh conflict    | Nhiều dev cùng sửa một file                     |

Dấu hiệu của một God Class:

- Class có hơn 20 method
- Làm nhiều việc khác nhau (ví dụ: xử lý business logic, tương tác database, gửi email, v.v.)
- Thông qua các tên class. Một số tên gọi God Class phổ biến: `OrderService`, `CommonProcessor`, `UserManager`, v.v.

Chính vì vậy, việc giữ cho class nhỏ gọn là rất quan trọng để đảm bảo code dễ hiểu, dễ sửa, và dễ test.

Không giống như function có thể xác định kích thước lớn/nhỏ bằng cách đếm số dòng.
Với class thì cần áp dụng một cách đếm khác, đó làm đếm *trách nhiệm*.

Ví dụ:
Bad

```php
namespace App\Services;

use App\Models\Order;
use App\Models\User;
use Illuminate\Http\UploadedFile;

class OrderService
{
    public function createOrder(array $data): Order
    {
        // Create order
    }

    public function cancelOrder(int $orderId): void
    {
        // Cancel order
    }

    public function calculateTotal(Order $order): float
    {
        // Calculate total
    }

    public function applyDiscount(Order $order): float
    {
        // Apply discount
    }

    public function reserveInventory(Order $order): void
    {
        // Reserve inventory
    }

    public function releaseInventory(Order $order): void
    {
        // Release inventory
    }

    // ... imagine 50+ more methods here
}

```

#### b. Nguyên tắc Single Responsibility Principle (SRP)

Nguyên tắc SRP là trạng thái mà một class hoặc module nên có một và chỉ một lý do để thay đổi.

Điều này không có nghĩa là một class chỉ được có một method. Một class có thể có nhiều method, nhưng các method đó nên cùng phục vụ một trách nhiệm chính.

Nói cách khác, khi requirement thay đổi, class đó chỉ nên bị ảnh hưởng bởi **một nhóm lý do cùng bản chất**.

Ví dụ

```php
namespace App\Services;

use App\Models\Order;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Storage;

class OrderManager
{
    public function createOrder(array $data): Order
    {
        // Validate data
        // Create order
        // Calculate total
        // Reserve inventory
        // Charge payment
        // Send confirmation email
        // Generate invoice PDF
        // Store invoice file
    }

    public function cancelOrder(int $orderId): void
    {
        // Cancel order
        // Release inventory
        // Refund payment
        // Send cancellation email
        // Write audit log
    }

    public function exportOrdersToCsv(): string
    {
        // Export orders
    }

    public function getOrderStatistics(): array
    {
        // Return report data
    }
}
```

Class này có nhiều lý do để thay đổi:

| Lý do thay đổi                  |           Nên thuộc class riêng không? |
| ------------------------------- | -------------------------------------: |
| Quy trình tạo order thay đổi    |          Có thể là `CreateOrderAction` |
| Quy tắc tính tổng tiền thay đổi |                 `OrderTotalCalculator` |
| Logic tồn kho thay đổi          |          `InventoryReservationService` |
| Cổng thanh toán thay đổi        | `PaymentService` hoặc `PaymentGateway` |
| Template email thay đổi         |                     `OrderEmailSender` |
| Logic export CSV thay đổi       |                     `OrderCsvExporter` |
| Logic thống kê thay đổi         |               `OrderStatisticsService` |

Class sau khi refactor lần 1

```php
namespace App\Services;
class OrderService
{
    public function createOrder(array $data): Order
    {
        // Validate data
        // Create order
        // Calculate total
        // Reserve inventory
        // Charge payment
        // Send confirmation email
        // Generate invoice PDF
        // Store invoice file
    }

    public function cancelOrder(int $orderId): void
    {
        // Cancel order
        // Release inventory
        // Refund payment
        // Send cancellation email
        // Write audit log
    }
}
```

Nếu logic của `createOrder` và `cancelOrder` vẫn còn phức tạp, có thể tiếp tục refactor bằng cách tách các phần logic ra thành các class riêng biệt, ví dụ:

```php
namespace App\Actions\Orders;

class CreateOrderAction
{
    public function __construct(
        private OrderTotalCalculator $totalCalculator,
        private InventoryReservationService $inventoryReservationService,
        private PaymentService $paymentService,
    ) {}

    public function execute(array $data): Order
    {
        $order = Order::create($data);

        $order->total = $this->totalCalculator->calculate($order);
        $order->save();

        $this->inventoryReservationService->reserve($order);
        $this->paymentService->charge($order);

        return $order;
    }
}
```

Cách này vẫn chưa tối ưu vì trong `execute` phụ thuộc trực tiếp vào Order. Khó test vì phải tạo một Order thật sự để test.

```php
class CreateOrderAction
{
    public function __construct(
        private OrderTotalCalculator $totalCalculator,
        private InventoryReservationService $inventoryReservationService,
        private PaymentService $paymentService,
        private Order $order,
    ) {}

    public function execute(array $data): Order
    {
        $order = $this->order->newInstance()->create($data);

        $order->total = $this->totalCalculator->calculate($order);
        $order->save();

        $this->inventoryReservationService->reserve($order);
        $this->paymentService->charge($order);

        return $order;
    }
}
```

SRP review checklist:

- Class này có thể được mô tả trong khoảng 25 từ không?
- Mô tả đó có phải dùng nhiều từ như `if`, `and`, `or`, `but` không?
- Tên class có cụ thể không?
- Class có đang dùng tên mơ hồ như `Manager`, `Processor`, `Helper`, `Common` không?
- Class này có bao nhiêu lý do để thay đổi?
- Các method trong class có cùng phục vụ một trách nhiệm chính không?
- Nếu tách class, tên các class mới có rõ nghĩa hơn không?

#### c. Mối liên kết

Mối liên kết (cohesion) có thể hiểu đơn giản là: Các thành bên trong một class có thật sự thuộc về nhau không?

Một class có cohesion cao khi:

- Các thuộc tính (attribute) đều phục vụ cho một mục đích
- Các method trong class thường xuyên sử dụng các thuộc tính đó

Ví dụ:

```php
class UserService {
    private UserRepository $userRepository;
    private SMTPEmailService $emailService;

    public function __construct(
        UserRepository $userRepository,
        SMTPEmailService $emailService
    ) {
        $this->userRepository = $userRepository;
        $this->emailService = $emailService;
    }

    public function register(array $data): User
    {
        // Validate data
        // Create user
        // Send welcome email
    }

    public function resetPassword(int $userId): void
    {
        // Generate reset token
        // Send password reset email
    }
}
```

Với class `UserService` này, có thể thấy rằng cả hai method `register` và `resetPassword` đều liên quan đến việc quản lý người dùng và gửi email. Các thuộc tính `$userRepository` và `$emailService` đều phục vụ cho mục đích này. Do đó, class này có cohesion cao.

Giả sử hệ thống có thêm 2 tính năng là `exportUserDataToCsv` và `generateUserReport`, nếu thêm chúng vào `UserService` thì sẽ làm giảm cohesion của class này, vì những tính năng này không liên quan trực tiếp đến việc quản lý người dùng hay gửi email.

Lúc này nên tách chúng ra thành một class riêng, ví dụ `UserDataExporter` hoặc `UserReportGenerator`, để giữ cho `UserService` có cohesion cao.

#### d. Thiết lập kết quả liên kết trong nhiều lớp nhỏ

Khi một class có nhiều trách nhiệm, có thể tách nó thành nhiều class nhỏ hơn, mỗi class phục vụ một mục đích cụ thể.
Khi refactor một hàm lớn thành nhiều hàm nhỏ, có thể vô tình làm class phình ra vì phải đưa nhiều biến local thành property để các hàm nhỏ dùng chung. Nếu các property đó chỉ phục vụ một nhóm method nhỏ, class bắt đầu mất cohesion. Khi đó nên tách class.

Ví dụ

```php
class UserService
{
    public function register(array $data): User
    {
        $email = $data['email'];
        $plainPassword = $data['password'];
        $role = 'member';

        $user = $this->userRepository->create([
            'email' => $email,
            'password' => bcrypt($plainPassword),
            'role' => $role,
        ]);

        $this->emailService->send(new WelcomeMail($user));

        return $user;
    }
}
```

Hàm `register` hơi dài và có nhiều bước, có thể refactor thành nhiều hàm nhỏ hơn:

```php
class UserService
{
    private string $email;
    private string $plainPassword;
    private string $role;
    private User $user;

    public function register(array $data): User
    {
        $this->email = $data['email'];
        $this->plainPassword = $data['password'];
        $this->role = 'member';

        $this->createUser();

        $this->sendWelcomeEmail();

        return $user;
    }

    private function createUser(): void
    {
        $this->user = $this->userRepository->create([
            'email' => $this->email,
            'password' => bcrypt($this->plainPassword),
            'role' => $this->role,
        ]);
    }

    private function sendWelcomeEmail(): void
    {
        $this->emailService->send(new WelcomeMail($this->user));
    }
}
```

Cách này tuy đã refactor thành nhiều hàm nhỏ hơn, nhưng class `UserService` đã trở nên phình to với nhiều property. Các property này chỉ phục vụ cho một nhóm method nhỏ, khiến class mất cohesion.

Giả sử `UserService` còn có thêm method `resetPassword` cũng cần dùng chung các property này, class sẽ càng phình to hơn nữa.

```php
class UserService
{
    private string $email;
    private string $plainPassword;
    private string $role;
    private User $user;
    private string $resetToken;

    public function register(array $data): User
    {
        $this->email = $data['email'];
        $this->plainPassword = $data['password'];
        $this->role = 'member';

        $this->createUser();

        $this->sendWelcomeEmail();

        return $user;
    }

    public function resetPassword(int $userId): void
    {
        $this->user = $this->userRepository->find($userId);
        $this->updatePassword($this->user, Str::random(12));

        $this->generateResetToken();
        
        $this->sendPasswordResetEmail();
    }

    private function createUser(): void
    {
        $this->user = $this->userRepository->create([
            'email' => $this->email,
            'password' => bcrypt($this->plainPassword),
            'role' => $this->role,
        ]);
    }

    private function sendWelcomeEmail(User $user): void
    {
        $this->emailService->send(new WelcomeMail($this->user));
    }

    private function updatePassword(User $user, string $newPassword): void
    {
        $user->password = bcrypt($newPassword);
        $this->userRepository->update($user);
    }

    private function generateResetToken(): string
    {
        // Logic generate reset token
        $this->resetToken = Str::random(60);
    }

    private function sendPasswordResetEmail(): void
    {
        // Logic send password reset email
    }
}
```

Lúc này `UserService` đã trở thành một God Class với nhiều trách nhiệm, nhiều property, và mất cohesion.
Cách tốt hơn là tách `register` và `resetPassword` thành các class riêng biệt, ví dụ `RegisterUserAction` và `ResetUserPasswordAction`.

```php
class RegisterUserAction
{
    const ROLE_MEMBER = 'member';

    private string $email;
    private string $plainPassword;
    private string $role;
    private User $user;

    public function __construct(
        private UserRepository $userRepository,
        private SMTPEmailService $emailService,
    ) {}

    public function execute(array $data): User
    {
        $this->email = $data['email'];
        $this->plainPassword = $data['password'];
        $this->role = self::ROLE_MEMBER;

        $this->createUser()
        
        $this->sendWelcomeEmail();

        return $user;
    }

    private function createUser(array $data): void
    {
        $this->user = $this->userRepository->create([
            'email' => $this->email,
            'password' => bcrypt($this->plainPassword),
            'role' => $this->role,
        ]);
    }

    private function sendWelcomeEmail(): void
    {
        $this->emailService->send(new WelcomeMail($this->user));
    }
}
```

```php
class ResetUserPasswordAction
{
    private User $user;
    private string $resetToken;

    public function __construct(
        private UserRepository $userRepository,
        private SMTPEmailService $emailService,
    ) {}

    public function execute(int $userId): void
    {
        $user = $this->userRepository->find($userId);
        $this->updatePassword($user, Str::random(12));

        $this->generateResetToken();

        $this->sendPasswordResetEmail();
    }

    private function updatePassword(User $user, string $newPassword): void
    {
        $user->password = bcrypt($newPassword);
        $this->user = $this->userRepository->update($user);
    }

    private function generateResetToken(): string
    {
        // Logic generate reset token
        $this->resetToken = Str::random(60);
    }

    private function sendPasswordResetEmail(): void
    {
        // Logic send password reset email
        $this->emailService->send(new PasswordResetMail($this->user, $this->resetToken));
    }
}
```

#### e. Tổ chức cho sự thay đổi và tách biệt sự thay đổi

Đối với hầu hết các hệ thống, thay đổi là điều luôn xảy ra. Mỗi thay đổi đều có thể mang lại những rủi ro khiến hệ thống hoạt động không đúng như mong muốn.
Do đó, việc tổ chức code giúp **giảm thiểu rủi ro** từ sự thay đổi là rất quan trọng.

- **Nguyên tắc đóng/mở (Open/Closed Principle - OCP)** là một trong những nguyên tắc giúp giảm thiểu rủi ro từ sự thay đổi.
  - Định nghĩa: các class nên mở cho việc mở rộng nhưng đóng cho việc sửa đổi.
  - Cấu trúc class lý tưởng cho phép thêm tính năng mới bằng cách thêm class con thay vì sửa đổi class hiện có.

- **Nguyên tắc đảo ngược phụ thuộc (Dependency Inversion Principle - DIP)** là một nguyên tắc giúp tách biệt sự thay đổi.
  - Định nghĩa: các class nên phụ thuộc vào abstraction (interface) thay vì implementation (class cụ thể). Điều này giúp tách biệt sự thay đổi, vì khi implementation thay đổi, chỉ cần sửa đổi class đó mà không ảnh hưởng đến các class khác, viết unit test cũng dễ dàng hơn.

Với các ví dụ ở [2.c Mối liên kết](#c-mối-liên-kết) và [2.d Thiết lập kết quả liên kết trong nhiều lớp nhỏ](#d-thiết-lập-kết-quả-liên-kết-trong-nhiều-lớp-nhỏ) đều vi phạm 2 nguyên tắc OCP và DIP.

Cùng phân tích chi tiết các vi phạm:

- Vi phạm OCP: Nếu muốn thay đổi cách gửi email. Ví dụ thay vì dùng SMTP, muốn chuyển sang dùng API của một dịch vụ email, phải sửa đổi `RegisterUserAction` để thay đổi logic gửi email, thay vì chỉ cần tạo một class con mới mà không cần sửa đổi `RegisterUserAction`.
- Vi phạm DIP: Phụ thuộc trực tiếp vào `SMTPEmailService`, implementation (class cụ thể). Gây ra các vấn đề:
  - Làm cho việc thay đổi implementation của email, ví dụ thêm MailgunEmailService (dịch vụ email khác) trở nên khó khăn và dễ gây ra lỗi.
  - Khi test, cũng phải phụ thuộc vào `SMTPEmailService`, khiến việc viết unit test trở nên khó khăn hơn.

Giải thích bằng ví dụ:

```php

class RegisterUserAction
{
    public function __construct(
        private UserRepository $userRepository,
        // Vi phạm DIP: phụ thuộc vào implementation cụ thể, không phải abstraction (interface)
        // Nếu muốn thay đổi sang MailgunEmailService, phải sửa đổi class này
        private SMTPEmailService $emailService,
    ) {}

    private function sendWelcomeEmail(): void
    {
        // Hàm này phụ thuộc trực tiếp vào SMTPEmailService
        // Nếu muốn đổi sang MailgunEmailService thì có thể phải sửa
        // trong trường hợp MailgunEmailService không có cùng method send() hoặc có cách gửi email khác
        $this->emailService->send(new WelcomeMail($this->user));
    }
}

```

Viết unit test cho `RegisterUserAction` cũng khó khăn vì phải phụ thuộc vào `SMTPEmailService`, một implementation cụ thể, thay vì có thể mock một interface chung.

```php
it('sends welcome email after registering user', function () {
    $emailServiceMock = Mockery::mock(SMTPEmailService::class);
    $emailServiceMock->shouldReceive('send')->once();

    $userRepositoryMock = Mockery::mock(UserRepositoryInterface::class);
    $userRepositoryMock->shouldReceive('create')->andReturn(new User());

    $action = new RegisterUserAction($userRepositoryMock, $emailServiceMock);
    $result = $action->execute([
        'email' => 'abc@gmail.com',
        'password' => 'secret',
    ]);

    expect($result)->toBeInstanceOf(User::class);
});

// Nếu muốn switch sang MailgunEmailService, phải sửa đổi unit test để mock MailgunEmailService thay vì SMTPEmailService
it('sends welcome email after registering user', function () {
    $emailServiceMock = Mockery::mock(MailgunEmailService::class);
    // Nếu MailgunEmailService có method send() giống SMTPEmailService thì có thể giữ nguyên,
    // nhưng nếu không thì phải sửa đổi để phù hợp với cách gửi email của MailgunEmailService
    $emailServiceMock->shouldReceive('send2')->once();

    $userRepositoryMock = Mockery::mock(UserRepositoryInterface::class);
    $userRepositoryMock->shouldReceive('create')->andReturn(new User());

    $action = new RegisterUserAction($userRepositoryMock, $emailServiceMock);
    $result = $action->execute([
        'email' => 'abc@gmail.com',
        'password' => 'secret',
    ]);

    expect($result)->toBeInstanceOf(User::class);
});

```

Giải pháp

```php
interface EmailServiceInterface
{
    public function send($mail): void;
}

class SMTPEmailService implements EmailServiceInterface
{
    public function send(Mail $mail): void
    {
        // Logic send email using SMTP
    }
}

class RegisterUserAction
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
        private EmailServiceInterface $emailService,
    ) {}

    public function execute(array $data): User
    {
        // Create user logic

        $this->sendWelcomeEmail($user);

        return $user;
    }

    private function sendWelcomeEmail(User $user): void
    {
        $this->emailService->send(new WelcomeMail($user));
    }
}
```

Trong ví dụ trên, `RegisterUserAction` phụ thuộc vào `EmailServiceInterface` thay vì một class cụ thể như `SMTPEmailService`.
Điều này giúp giảm thiểu rủi ro từ sự thay đổi, vì khi cần thêm một cách gửi email mới, chỉ cần tạo một class mới implement `EmailServiceInterface` mà không cần sửa đổi `RegisterUserAction`.

```php
class MailgunEmailService implements EmailServiceInterface
{
    public function send(Mail $mail): void
    {
        // Logic send email using Mailgun API
    }
}
```

Khi đó, nếu muốn sử dụng `MailgunEmailService` thay vì `SMTPEmailService`, chỉ cần thay đổi cấu hình dependency injection để inject `MailgunEmailService` vào `RegisterUserAction` mà không cần sửa đổi code của `RegisterUserAction`.

```php
// Lravel service provider cấu hình để inject MailgunEmailService cho EmailServiceInterface
class AppServiceProvider extends ServiceProvider
{
    public function register()
    {
        $this->app->bind(EmailServiceInterface::class, MailgunEmailService::class);
    }
}

// Hoặc nếu muốn switch thủ công
$registerUserUsingMailgun = new RegisterUserAction($userRepository, new MailgunEmailService());
$resigterUserUsingSMTP = new RegisterUserAction($userRepository, new SMTPEmailService());

```

Viết unit test cho `RegisterUserAction` cũng dễ dàng hơn vì có thể mock `EmailServiceInterface` mà không cần phụ thuộc vào một implementation cụ thể.

Khi các implementation như `SMTPEmailService` và `MailgunEmailService` có thay đổi thì cũng không ảnh hưởng đến unit test của `RegisterUserAction`.

```php
it('sends welcome email after registering user', function () {
    $emailServiceMock = Mockery::mock(EmailServiceInterface::class);
    $emailServiceMock->shouldReceive('send')->once();

    $userRepositoryMock = Mockery::mock(UserRepositoryInterface::class);
    $userRepositoryMock->shouldReceive('create')->andReturn(new User());

    $action = new RegisterUserAction($userRepositoryMock, $emailServiceMock);
    $result = $action->execute([
        'email' => 'abc@gmail.com',
        'password' => 'secret',
    ]);

    expect($result)->toBeInstanceOf(User::class);
});
```

## 2. Câu hỏi thảo luận

## 3. Kết luận

### 3.1. Tóm tắt nội dung đã thống nhất

### 3.2 Conding Conventions của chương 10
