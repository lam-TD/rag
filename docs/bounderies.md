# Clean Code – Chương 8: Boundaries
## Tài liệu thảo luận nhóm + Team Convention (kèm ví dụ PHP)

---

## 1. Mục đích tài liệu

Tài liệu này giúp team thống nhất cách hiểu và cách áp dụng nội dung của **Chương 8 – Boundaries** trong dự án PHP.

Mục tiêu chính:

- hiểu “boundary” là gì trong code thực tế
- biết vì sao không nên để thư viện bên thứ ba đi xuyên qua toàn bộ hệ thống
- biết cách dùng **Wrapper**, **Adapter**, **DTO**, **Interface** để giữ mã sạch
- biết khi nào nên viết **learning tests**
- chuyển các ý trong sách thành **quy ước review code của team**

---

## 2. Boundary là gì?

Trong dự án PHP, **boundary** là nơi hệ thống của chúng ta tiếp giáp với thứ mà chúng ta **không hoàn toàn kiểm soát**.

Ví dụ rất thường gặp:

- package cài qua Composer
- SDK bên thứ ba: Stripe, AWS, Redis, Elasticsearch
- HTTP API của đối tác
- API của team khác trong nội bộ công ty
- framework facade/helper có API quá rộng
- dữ liệu trả về dạng `array` / JSON từ bên ngoài

### Tư tưởng cốt lõi

> Mã nghiệp vụ nên phụ thuộc vào điều team kiểm soát.
> Không nên để business code nói trực tiếp bằng “ngôn ngữ” của thư viện hoặc API bên ngoài.

---

## 3. Vấn đề khi dùng trực tiếp mã nguồn bên thứ ba

Nếu để SDK, response raw, exception của bên ngoài đi xuyên qua nhiều layer, hệ thống sẽ gặp các vấn đề sau:

### 3.1. Business code biết quá nhiều chi tiết kỹ thuật

Ví dụ service nghiệp vụ biết luôn:

- tên class của SDK
- cấu trúc request của bên thứ ba
- key response như `tracking_no`, `risk_level`, `payment_url`
- exception riêng của thư viện

Khi đó business code bị dính chặt vào implementation.

### 3.2. Khó thay thế thư viện hoặc nhà cung cấp

Nếu sau này đổi:

- Stripe sang cổng thanh toán khác
- S3 sang local storage
- Redis client này sang Redis client khác
- API của partner v1 sang v2

thì phải sửa nhiều nơi.

### 3.3. Dễ bị lạm dụng hoặc dùng sai

Khi truyền `array` hoặc object raw đi khắp nơi, mọi chỗ đều có thể:

- đọc field không nên phụ thuộc
- sửa dữ liệu ngoài ý muốn
- dựa vào chi tiết nội bộ của bên thứ ba

### 3.4. Khó test

Muốn test business logic nhưng lại phải kéo theo:

- network
- SDK thật
- fake phức tạp
- mock theo kiểu phụ thuộc implementation

---

## 4. Nguyên tắc áp dụng cho team

### 4.1. Chỉ một số ít lớp được phép “biết” bên ngoài

Các chi tiết về thư viện bên thứ ba nên được gom vào các lớp như:

- `StripePaymentGateway`
- `AwsS3FileStorage`
- `HttpCustomerRiskService`
- `RedisUserProfileCache`

Các lớp này là nơi tiếp xúc với boundary.

### 4.2. Business code chỉ làm việc với interface nội bộ

Business code nên phụ thuộc vào các abstraction do team tự định nghĩa, ví dụ:

- `PaymentGateway`
- `FileStorage`
- `CustomerRiskService`
- `Mailer`

### 4.3. Map dữ liệu ngoài vào kiểu dữ liệu nội bộ càng sớm càng tốt

Thay vì truyền raw response đi khắp nơi, hãy chuyển ngay sang:

- DTO
- Value Object
- Domain Object

### 4.4. Không làm rò rỉ exception của thư viện bên ngoài ra domain

Nên wrap exception của thư viện thành exception nội bộ có ý nghĩa nghiệp vụ hoặc hạ tầng.

### 4.5. Viết learning tests cho thư viện khó hiểu hoặc có rủi ro upgrade

Đặc biệt nên áp dụng với:

- CSV / Excel parser
- HTTP client
- date/time library
- storage SDK
- markdown/html sanitizer
- queue / cache client

---

## 5. Ví dụ thực tế 1 – Tích hợp cổng thanh toán

### 5.1. Cách viết chưa sạch

```php
use Stripe\StripeClient;

final class OrderService
{
    public function checkout(Order $order): array
    {
        $stripe = new StripeClient($_ENV['STRIPE_SECRET']);

        $session = $stripe->checkout->sessions->create([
            'mode' => 'payment',
            'line_items' => [[
                'price_data' => [
                    'currency' => 'usd',
                    'product_data' => ['name' => $order->productName()],
                    'unit_amount' => $order->amountInCents(),
                ],
                'quantity' => 1,
            ]],
            'success_url' => 'https://example.com/success',
            'cancel_url' => 'https://example.com/cancel',
        ]);

        return [
            'session_id' => $session->id,
            'url' => $session->url,
        ];
    }
}
```

### 5.2. Vấn đề

- `OrderService` biết quá nhiều về Stripe
- business code bị phụ thuộc vào cấu trúc request của Stripe
- trả về `array` làm lộ chi tiết response
- đổi cổng thanh toán sẽ phải sửa trực tiếp business service

### 5.3. Cách viết sạch hơn

#### Interface nội bộ

```php
interface PaymentGateway
{
    public function createCheckoutSession(PaymentRequest $request): PaymentSession;
}
```

#### DTO nội bộ

```php
final class PaymentRequest
{
    public function __construct(
        public readonly string $orderId,
        public readonly string $productName,
        public readonly int $amountInCents,
        public readonly string $currency,
        public readonly string $successUrl,
        public readonly string $cancelUrl,
    ) {}
}
```

```php
final class PaymentSession
{
    public function __construct(
        public readonly string $id,
        public readonly string $checkoutUrl,
    ) {}
}
```

#### Business code chỉ biết interface

```php
final class OrderService
{
    public function __construct(
        private PaymentGateway $paymentGateway,
    ) {}

    public function checkout(Order $order): PaymentSession
    {
        $request = new PaymentRequest(
            orderId: $order->id(),
            productName: $order->productName(),
            amountInCents: $order->amountInCents(),
            currency: 'usd',
            successUrl: 'https://example.com/success',
            cancelUrl: 'https://example.com/cancel',
        );

        return $this->paymentGateway->createCheckoutSession($request);
    }
}
```

#### Adapter nói chuyện với Stripe

```php
use Stripe\StripeClient;

final class StripePaymentGateway implements PaymentGateway
{
    public function __construct(
        private StripeClient $stripe,
    ) {}

    public function createCheckoutSession(PaymentRequest $request): PaymentSession
    {
        $session = $this->stripe->checkout->sessions->create([
            'mode' => 'payment',
            'line_items' => [[
                'price_data' => [
                    'currency' => $request->currency,
                    'product_data' => ['name' => $request->productName],
                    'unit_amount' => $request->amountInCents,
                ],
                'quantity' => 1,
            ]],
            'success_url' => $request->successUrl,
            'cancel_url' => $request->cancelUrl,
            'metadata' => [
                'order_id' => $request->orderId,
            ],
        ]);

        return new PaymentSession(
            id: $session->id,
            checkoutUrl: $session->url,
        );
    }
}
```

### 5.4. Điều rút ra

`OrderService` đang nói bằng ngôn ngữ nghiệp vụ của hệ thống, không nói bằng ngôn ngữ Stripe.

---

## 6. Ví dụ thực tế 2 – Không truyền `array` raw đi khắp hệ thống

Trong PHP, `array` thường đóng vai trò giống `Map` trong ví dụ của sách.

### 6.1. Cách làm dễ gặp

```php
final class ShippingService
{
    public function createShipment(array $payload): array
    {
        return [
            'tracking_no' => 'VN123456',
            'status' => 'created',
            'carrier_code' => 'ghn',
            'raw' => ['debug' => '...'],
        ];
    }
}
```

Nơi gọi:

```php
$result = $shippingService->createShipment($payload);

if ($result['status'] === 'created') {
    $tracking = $result['tracking_no'];
}
```

### 6.2. Vấn đề

- dễ typo key
- không biết field nào là bắt buộc
- response thay đổi là hỏng nhiều nơi
- các chỗ khác có thể dựa luôn vào `raw`

### 6.3. Cách sạch hơn

```php
final class ShipmentResult
{
    public function __construct(
        public readonly string $trackingNumber,
        public readonly string $status,
        public readonly string $carrier,
    ) {}
}
```

```php
interface ShippingGateway
{
    public function createShipment(ShipmentRequest $request): ShipmentResult;
}
```

```php
final class GhnShippingGateway implements ShippingGateway
{
    public function createShipment(ShipmentRequest $request): ShipmentResult
    {
        $response = [
            'tracking_no' => 'VN123456',
            'status' => 'created',
            'carrier_code' => 'ghn',
        ];

        return new ShipmentResult(
            trackingNumber: $response['tracking_no'],
            status: $response['status'],
            carrier: $response['carrier_code'],
        );
    }
}
```

### 6.4. Rule cho team

- không trả về `array` raw từ adapter nếu response đó là dữ liệu quan trọng của nghiệp vụ
- ưu tiên DTO khi dữ liệu có cấu trúc ổn định
- chỉ giữ `raw` ở adapter hoặc logging/debug, không phát tán sang service nghiệp vụ

---

## 7. Ví dụ thực tế 3 – Learning Tests

### 7.1. Khi nào cần learning tests?

Khi team đang dùng một thư viện mà:

- tài liệu khó hiểu
- API quá rộng
- có hành vi dễ hiểu sai
- sắp upgrade version
- business flow phụ thuộc vào chi tiết hành vi của thư viện

### 7.2. Ví dụ với thư viện đọc CSV

```php
use League\Csv\Reader;
use PHPUnit\Framework\TestCase;

final class LeagueCsvLearningTest extends TestCase
{
    public function test_it_reads_header_and_records(): void
    {
        $csv = Reader::createFromString("name,email\nJoyce,joyce@example.com");
        $csv->setHeaderOffset(0);

        $records = iterator_to_array($csv->getRecords());

        $this->assertCount(1, $records);
        $this->assertSame('Joyce', $records[0]['name']);
        $this->assertSame('joyce@example.com', $records[0]['email']);
    }

    public function test_it_returns_empty_records_when_only_header_exists(): void
    {
        $csv = Reader::createFromString("name,email\n");
        $csv->setHeaderOffset(0);

        $records = iterator_to_array($csv->getRecords());

        $this->assertCount(0, $records);
    }
}
```

### 7.3. Giá trị thực tế

- giúp team hiểu đúng package trước khi đưa vào production
- khi nâng version package, chỉ cần chạy test để phát hiện thay đổi hành vi
- test này vừa là kiểm chứng, vừa là tài liệu sống cho team

### 7.4. Convention đề xuất

Team nên tạo thư mục riêng cho learning tests, ví dụ:

```text
tests/
  Learning/
    LeagueCsvLearningTest.php
    StripeSdkLearningTest.php
    CarbonBehaviorLearningTest.php
```

---

## 8. Ví dụ thực tế 4 – API chưa tồn tại nhưng vẫn tiếp tục phát triển

Đây là tình huống rất thật trong dự án nhiều team.

### Bối cảnh

Team A đang cần gọi API chấm điểm rủi ro khách hàng, nhưng Team B vẫn chưa hoàn tất API.

### Cách tiếp cận tốt

Tự định nghĩa interface theo nhu cầu của nghiệp vụ.

```php
interface CustomerRiskService
{
    public function getRiskLevel(string $customerId): RiskLevel;
}
```

```php
final class RiskLevel
{
    public function __construct(
        public readonly string $level,
        public readonly int $score,
    ) {}
}
```

Business code:

```php
final class LoanApprovalService
{
    public function __construct(
        private CustomerRiskService $customerRiskService,
    ) {}

    public function approve(string $customerId): bool
    {
        $risk = $this->customerRiskService->getRiskLevel($customerId);

        return $risk->level !== 'high';
    }
}
```

Trong lúc API thật chưa có, dùng fake:

```php
final class FakeCustomerRiskService implements CustomerRiskService
{
    public function getRiskLevel(string $customerId): RiskLevel
    {
        return new RiskLevel(level: 'low', score: 20);
    }
}
```

Khi API thật sẵn sàng, viết adapter:

```php
use GuzzleHttp\ClientInterface;

final class HttpCustomerRiskService implements CustomerRiskService
{
    public function __construct(
        private ClientInterface $httpClient,
    ) {}

    public function getRiskLevel(string $customerId): RiskLevel
    {
        $response = $this->httpClient->request('GET', "/risk-score/{$customerId}");
        $data = json_decode((string) $response->getBody(), true);

        return new RiskLevel(
            level: $data['risk_level'],
            score: $data['risk_score'],
        );
    }
}
```

### Điều rút ra

- không bị block bởi thứ chưa hoàn chỉnh
- business code vẫn ổn định
- chỉ cần sửa adapter nếu API thật khác kỳ vọng ban đầu

---

## 9. Ví dụ thực tế 5 – Không để exception của thư viện rò rỉ ra ngoài

### 9.1. Cách chưa sạch

```php
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

final class NotificationService
{
    public function __construct(private Client $client) {}

    public function sendWelcomeEmail(string $email): void
    {
        try {
            $this->client->post('/send', [
                'json' => [
                    'template' => 'welcome',
                    'email' => $email,
                ],
            ]);
        } catch (RequestException $e) {
            throw $e;
        }
    }
}
```

### 9.2. Vấn đề

Nếu nơi gọi phải `catch RequestException`, tức là boundary đã bị rò rỉ ra ngoài.

### 9.3. Cách tốt hơn

```php
interface Mailer
{
    public function sendWelcomeEmail(string $email): void;
}
```

```php
final class MailDeliveryFailed extends RuntimeException
{
}
```

```php
use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\GuzzleException;

final class ApiMailer implements Mailer
{
    public function __construct(
        private ClientInterface $client,
    ) {}

    public function sendWelcomeEmail(string $email): void
    {
        try {
            $this->client->request('POST', '/send', [
                'json' => [
                    'template' => 'welcome',
                    'email' => $email,
                ],
            ]);
        } catch (GuzzleException $e) {
            throw new MailDeliveryFailed(
                message: 'Cannot send welcome email.',
                previous: $e,
            );
        }
    }
}
```

### Rule cho team

- layer nghiệp vụ không phụ thuộc vào exception class của SDK bên ngoài
- exception của thư viện chỉ nên xuất hiện trong adapter hoặc infrastructure layer
- nếu cần, wrap thành exception nội bộ có ý nghĩa rõ ràng hơn

---

## 10. Áp dụng vào Laravel / PHP backend

### 10.1. File storage

Không nên để business code gọi trực tiếp:

```php
Storage::disk('s3')->put($path, $content);
```

Nên bọc lại:

```php
interface FileStorage
{
    public function put(string $path, string $content): void;
    public function url(string $path): string;
}
```

### 10.2. Queue

Thay vì service nghiệp vụ biết luôn `dispatch()` hay queue name:

```php
interface ReportJobDispatcher
{
    public function dispatchGenerateMonthlyReport(int $reportId): void;
}
```

### 10.3. Cache

Không nên để business code biết format Redis key:

```php
$redis->set("user:{$id}:profile", json_encode($data));
```

Nên dùng abstraction:

```php
interface UserProfileCache
{
    public function put(UserProfile $profile): void;
    public function getByUserId(int $userId): ?UserProfile;
}
```

### 10.4. API client

Không trả nguyên JSON/array response từ partner vào service nghiệp vụ. Hãy map sang DTO của hệ thống.

---

## 11. Team Convention đề xuất

## 11.1. Naming

### Interface cho boundary

Ưu tiên các tên theo ý nghĩa nghiệp vụ hoặc khả năng hệ thống cần:

- `PaymentGateway`
- `FileStorage`
- `CustomerRiskService`
- `Mailer`
- `ShippingGateway`

Không ưu tiên tên quá lệ thuộc implementation, ví dụ:

- `StripeServiceInterface`
- `AwsServiceInterface`
- `GuzzleClientWrapper`

Lý do: interface nên thể hiện **điều hệ thống cần**, không phải **tên thư viện đang dùng**.

### Adapter / implementation

Tên implementation có thể gắn với nhà cung cấp:

- `StripePaymentGateway`
- `AwsS3FileStorage`
- `HttpCustomerRiskService`
- `ApiMailer`
- `GhnShippingGateway`

### DTO / Value Object

Đặt tên theo dữ liệu có ý nghĩa nghiệp vụ:

- `PaymentRequest`
- `PaymentSession`
- `ShipmentResult`
- `RiskLevel`

---

## 11.2. Cấu trúc thư mục gợi ý

```text
src/
  Domain/
    Payment/
      PaymentGateway.php
      PaymentRequest.php
      PaymentSession.php
  Application/
    Order/
      OrderService.php
  Infrastructure/
    Payment/
      StripePaymentGateway.php
    Mail/
      ApiMailer.php
    Shipping/
      GhnShippingGateway.php
tests/
  Unit/
  Integration/
  Learning/
```

---

## 11.3. Rule bắt buộc khi review code

### Rule 1
Không inject SDK client trực tiếp vào domain service hoặc application service nếu có thể tách qua boundary interface.

### Rule 2
Không truyền `array` raw của bên thứ ba xuyên qua nhiều layer nếu dữ liệu đó có ý nghĩa nghiệp vụ.

### Rule 3
Không để controller/service/use case biết key response đặc thù của partner như:

- `tracking_no`
- `risk_score`
- `payment_url`
- `carrier_code`

### Rule 4
Không để exception class của thư viện bên thứ ba đi xuyên qua layer nghiệp vụ.

### Rule 5
Boundary mới hoặc thư viện có rủi ro cao nên có learning tests.

### Rule 6
Nếu API của team khác chưa xong, ưu tiên tự định nghĩa interface nội bộ trước, sau đó dùng adapter để nối khi API thật sẵn sàng.

---

## 11.4. Khi nào có thể dùng trực tiếp thư viện mà không cần wrapper?

Không phải mọi chỗ đều phải bọc.

Có thể chấp nhận dùng trực tiếp khi:

- phạm vi rất nhỏ
- chỉ xuất hiện ở 1 chỗ duy nhất
- chi phí trừu tượng hóa lớn hơn lợi ích
- chưa có dấu hiệu thay đổi hoặc reuse

Ví dụ:

- một helper format thời gian đơn giản
- một package chỉ dùng nội bộ trong một file migration/tool script

Tuy nhiên, nếu thư viện đó đi vào business flow chính, nên cân nhắc bọc lại sớm.

---

## 12. Checklist review nhanh cho team

Khi review một đoạn code có tích hợp bên ngoài, hãy hỏi:

1. Class này có đang biết quá nhiều về thư viện bên ngoài không?
2. Có đang trả về `array` raw hoặc object raw của SDK cho nhiều nơi khác dùng không?
3. Nếu đổi provider, phải sửa bao nhiêu file?
4. Có đang làm rò rỉ exception của thư viện ra ngoài không?
5. Có thể map response sang DTO nội bộ sớm hơn không?
6. API/SDK này đã có learning test chưa?
7. Interface hiện tại đang nói bằng ngôn ngữ nghiệp vụ hay bằng tên vendor?

---

## 13. Câu hỏi thảo luận nhóm

### Câu 1
Trong dự án hiện tại của team, đâu là boundary có rủi ro cao nhất?

Gợi ý trả lời:

- cổng thanh toán
- file storage
- HTTP API của partner
- queue / cache
- package parser dữ liệu

### Câu 2
Có chỗ nào đang truyền `array` hoặc JSON raw đi quá xa trong hệ thống không?

Gợi ý trả lời:

- response của API đối tác
- dữ liệu webhook
- dữ liệu từ Redis/cache
- payload upload/import

### Câu 3
Nếu ngày mai phải đổi một thư viện đang dùng, chỗ nào sẽ đau nhất?

Gợi ý trả lời:

Nơi nào business code đang phụ thuộc trực tiếp vào SDK hoặc cấu trúc response của vendor thì nơi đó đau nhất.

### Câu 4
Trong hệ thống hiện tại, team đã có learning test nào chưa?

Gợi ý trả lời:

Nếu chưa có, hãy chọn 1 package dễ gây lỗi khi upgrade để làm trước.

### Câu 5
Có API nội bộ nào của team khác chưa hoàn chỉnh nhưng team mình vẫn đang phải phụ thuộc không?

Gợi ý trả lời:

Nếu có, nên tự định nghĩa interface trước để business code không bị block.

---

## 14. Kết luận

Tinh thần chính của chương Boundaries có thể tóm gọn như sau:

- gom sự phụ thuộc vào bên ngoài vào một số ít điểm có kiểm soát
- không để business code lệ thuộc trực tiếp vào SDK, response, exception của bên thứ ba
- map dữ liệu bên ngoài sang kiểu dữ liệu nội bộ càng sớm càng tốt
- dùng learning tests để hiểu và bảo vệ hành vi của thư viện
- ưu tiên phụ thuộc vào abstraction do team kiểm soát

### Một câu nhớ nhanh cho team

> Business code nên nói bằng ngôn ngữ nghiệp vụ của hệ thống, không nên nói bằng ngôn ngữ của vendor.

---

## 15. Hành động đề xuất sau buổi thảo luận

- chọn 1 boundary trong dự án thật để refactor thử
- tạo 1 learning test cho package đang dùng nhiều
- bổ sung checklist boundary vào code review
- thống nhất naming cho interface và adapter trong toàn team

