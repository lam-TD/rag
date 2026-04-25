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
        if (! in_array($file->extension(), ['pdf', 'docx', 'txt'], true)) {
            throw new \InvalidArgumentException('Unsupported file type.');
        }

        if ($file->getSize() > 10 * 1024 * 1024) {
            throw new \InvalidArgumentException('File size must not exceed 10MB.');
        }
    }

    protected function buildStoragePath(UploadedFile $file): string
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

Giả sử hệ thống cần test DocumentUploadService, để có thể test được `validateFile` và `buildStoragePath` team đã đổi chúng thành `protected` để có thể tạo một class con trong test và gọi được các method này. Đây là một sai lầm phổ biến.

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

Cũng giống như function, một class nên được thiết kế nhỏ gọn.
Nhưng với function có thể xác định kích thước lớn nhỏ bằng cách đếm số dòng.
Với class thì cần áp dụng một cách đếm khác, đó làm đếm *trách nhiệm*.


## 2. Câu hỏi thảo luận