# Các ý chính và khái niệm chính – Clean Code: Chương Systems

## 1. Hệ thống phải sạch ở cấp độ kiến trúc

Chương **Systems** nhấn mạnh rằng Clean Code không chỉ áp dụng cho từng hàm, từng class, mà còn phải áp dụng ở cấp độ toàn hệ thống.

Một hệ thống sạch cần có sự tách biệt rõ ràng giữa:

- Logic nghiệp vụ
- Cách khởi tạo object
- Cơ chế lưu trữ dữ liệu
- Bảo mật
- Logging
- Transaction
- Framework
- Infrastructure

Mục tiêu là giúp hệ thống dễ hiểu, dễ kiểm thử, dễ mở rộng và dễ thay đổi.

---

## 2. Tách biệt việc xây dựng hệ thống khỏi việc sử dụng

Một hệ thống nên tách quá trình **xây dựng object và kết nối dependency** khỏi quá trình **sử dụng object để xử lý nghiệp vụ**.

Ý chính:

- Class nghiệp vụ không nên tự tạo dependency.
- Việc khởi tạo dependency nên được đưa ra bên ngoài.
- Object nên nhận dependency đã được chuẩn bị sẵn.
- Điều này giúp giảm coupling và tăng khả năng test.

Khái niệm liên quan:

- Separation of Main
- Dependency Injection
- Service Container
- Service Provider
- Object construction
- Runtime logic

Ví dụ trong Laravel:

- Binding dependency trong `ServiceProvider`
- Inject service qua constructor
- Không dùng `new SomeService()` trực tiếp trong business logic

---

## 3. Dependency Injection là cơ chế quan trọng để tách biệt hệ thống

**Dependency Injection** là kỹ thuật đưa dependency từ bên ngoài vào class thay vì để class tự tạo dependency.

Ý chính:

- Class trở nên thụ động hơn.
- Class chỉ tập trung vào nghiệp vụ chính.
- Dependency có thể được thay đổi dễ dàng.
- Unit test trở nên đơn giản hơn vì có thể mock dependency.

Khái niệm liên quan:

- DI
- Constructor Injection
- Interface Binding
- Inversion of Control
- Service Container

Trong Laravel, DI thường được thực hiện thông qua:

- Constructor injection
- Method injection
- Interface binding trong `AppServiceProvider`

---

## 4. Factory Pattern giúp kiểm soát việc tạo object khi runtime

Factory được sử dụng khi ứng dụng cần tạo object dựa trên điều kiện tại thời điểm chạy.

Ý chính:

- Business code có thể quyết định **khi nào** cần object.
- Factory quyết định **tạo object như thế nào**.
- Giúp tránh việc rải rác logic `if/else`, `match`, `new` trong service nghiệp vụ.

Khái niệm liên quan:

- Factory Pattern
- Abstract Factory
- Object creation
- Runtime decision
- Encapsulation of construction logic

Ví dụ trong Laravel:

- `PaymentGatewayFactory`
- `NotificationChannelFactory`
- `StorageDriverFactory`
- `EmbeddingProviderFactory`

---

## 5. Hệ thống có thể mở rộng dần nếu tách biệt tốt các mối quan tâm

Tác giả nhấn mạnh rằng phần mềm khác với công trình vật lý. Phần mềm có thể bắt đầu đơn giản, sau đó phát triển dần nếu kiến trúc được tách biệt tốt.

Ý chính:

- Không nên thiết kế quá lớn ngay từ đầu.
- Không nên cố dự đoán toàn bộ tương lai của hệ thống.
- Nên bắt đầu với thiết kế đơn giản nhất có thể hoạt động.
- Khi yêu cầu phát triển, hệ thống có thể mở rộng từng bước.

Khái niệm liên quan:

- Scaling Up
- Separation of Concerns
- Incremental architecture
- Evolutionary design
- BDUF — Big Design Up Front

---

## 6. Không nên thiết kế quá lớn ngay từ đầu

Chương này cảnh báo về việc cố xây dựng kiến trúc quá phức tạp ngay từ đầu.

Ý chính:

- Thiết kế quá sớm thường dựa trên thông tin chưa đầy đủ.
- Kiến trúc quá lớn làm tăng chi phí bảo trì.
- Nhiều abstraction được tạo ra trước khi có nhu cầu thật sự.
- Hệ thống nên được thiết kế để có thể thay đổi, không phải để đoán trước mọi thứ.

Khái niệm liên quan:

- Big Design Up Front
- Over-engineering
- YAGNI
- Simple Design
- Delayed decision

---

## 7. Cross-Cutting Concerns cần được tách khỏi logic nghiệp vụ

**Cross-cutting concerns** là các mối quan tâm kỹ thuật xuất hiện ở nhiều nơi trong hệ thống.

Ví dụ:

- Logging
- Authentication
- Authorization
- Transaction
- Caching
- Validation
- Error handling
- Security
- Rate limiting
- Monitoring

Ý chính:

- Những concern này không nên bị trộn trực tiếp vào business logic.
- Nếu để rải rác trong nhiều class, hệ thống sẽ khó đọc và khó thay đổi.
- Nên có cơ chế riêng để xử lý chúng.

Trong Laravel, có thể xử lý bằng:

- Middleware
- Form Request
- Policy / Gate
- Event / Listener
- Job
- Decorator
- Pipeline

---

## 8. AOP giúp xử lý các concern cắt ngang hệ thống

**Aspect-Oriented Programming** là một cách tiếp cận giúp tách các concern cắt ngang khỏi logic nghiệp vụ chính.

Ý chính:

- Business logic không nên biết quá nhiều về logging, security, transaction.
- Các concern kỹ thuật có thể được “bọc” xung quanh logic chính.
- Điều này giúp code nghiệp vụ sạch và tập trung hơn.

Khái niệm liên quan:

- AOP
- Aspect
- Cross-cutting concerns
- Proxy
- Decorator
- Interceptor

Trong Laravel, không có AOP mạnh như Java/Spring, nhưng có thể áp dụng tư duy tương tự bằng:

- Middleware
- Event / Listener
- Decorator
- Pipeline
- Observer

---

## 9. Logic nghiệp vụ nên được giữ thuần túy

Chương Systems khuyến khích viết logic nghiệp vụ dưới dạng các object thuần túy, ít phụ thuộc vào framework.

Trong Java, khái niệm này thường gọi là **POJO — Plain Old Java Object**.

Trong Laravel/PHP, có thể hiểu là:

- Plain PHP Class
- Domain Service
- Value Object
- Business Rule Class

Ý chính:

- Logic nghiệp vụ không nên phụ thuộc quá sâu vào Laravel, Eloquent, Facade hoặc HTTP layer.
- Class nghiệp vụ càng thuần túy thì càng dễ test.
- Framework nên là công cụ hỗ trợ, không nên chi phối toàn bộ thiết kế nghiệp vụ.

Ví dụ Laravel:

- `OrderTotalCalculator`
- `DiscountPolicy`
- `ShippingFeeCalculator`
- `TaxCalculator`
- `PaymentRule`

---

## 10. Proxy và Decorator giúp thêm hành vi mà không làm bẩn class chính

Proxy hoặc Decorator có thể được dùng để bọc object thật và thêm các hành vi kỹ thuật xung quanh nó.

Ý chính:

- Class chính vẫn giữ logic nghiệp vụ thuần túy.
- Các hành vi phụ như cache, log, retry, permission check có thể được tách ra.
- Giúp mở rộng hành vi mà không sửa class gốc.

Khái niệm liên quan:

- Proxy Pattern
- Decorator Pattern
- Wrapper
- Interceptor
- Open/Closed Principle

Ví dụ trong Laravel:

- `CachedProductReader`
- `LoggingPaymentGateway`
- `RetryableHttpClient`
- `AuthorizedDocumentReader`

---

## 11. Nên trì hoãn các quyết định quan trọng đến thời điểm phù hợp

Một kiến trúc tốt cho phép đội ngũ trì hoãn những quyết định kỹ thuật quan trọng cho đến khi có đủ thông tin.

Ý chính:

- Không nên quyết định quá sớm khi chưa hiểu rõ nhu cầu thật.
- Việc quyết định quá sớm có thể làm hệ thống bị khóa vào một công nghệ cụ thể.
- Tạo abstraction hợp lý giúp thay đổi công nghệ dễ hơn sau này.

Khái niệm liên quan:

- Delayed decision
- Abstraction
- Interface
- Replaceable implementation
- Technology independence

Ví dụ:

- Chưa cần quyết định ngay dùng local storage, S3 hay MinIO.
- Có thể tạo interface `FileStorage`.
- Business logic chỉ phụ thuộc vào `FileStorage`, không phụ thuộc trực tiếp vào driver cụ thể.

---

## 12. Sử dụng tiêu chuẩn và framework một cách khôn ngoan

Chương này nhấn mạnh rằng không nên chạy theo tiêu chuẩn, framework hoặc pattern chỉ vì chúng phổ biến.

Ý chính:

- Tiêu chuẩn chỉ có giá trị khi giải quyết vấn đề thực tế.
- Framework không nên làm mờ logic nghiệp vụ.
- Pattern không nên được áp dụng máy móc.
- Kiến trúc tốt là kiến trúc phục vụ nhu cầu thật của hệ thống.

Khái niệm liên quan:

- Standards
- Frameworks
- Convention
- Pattern misuse
- Pragmatic design

Ví dụ trong Laravel:

- Không phải model nào cũng cần Repository.
- Không phải nghiệp vụ nào cũng cần Service class.
- Không phải logic nào cũng nên đưa vào Model.
- Không nên tạo abstraction nếu chưa có nhu cầu thay đổi rõ ràng.

---

## 13. DSL giúp code gần với ngôn ngữ nghiệp vụ hơn

**DSL — Domain-Specific Language** là cách viết code gần với ngôn ngữ của miền nghiệp vụ.

Ý chính:

- Code nên thể hiện rõ ý định nghiệp vụ.
- Người đọc không nên phải giải mã quá nhiều điều kiện kỹ thuật.
- Các method nghiệp vụ rõ nghĩa giúp giảm hiểu nhầm giữa dev và business.

Khái niệm liên quan:

- DSL
- Domain language
- Business-readable code
- Expressive code
- Intention-revealing method

Ví dụ:

Thay vì viết điều kiện kỹ thuật:

```php
if ($order->status === 'paid' && $order->shipped_at === null) {
    // ...
}
```

Có thể viết gần với nghiệp vụ hơn:

```php
if ($order->isReadyToShip()) {
    // ...
}
```

---

# Danh sách khái niệm chính của chương Systems

- Systems
- Separation of Main
- Separation of Concerns
- Dependency Injection
- Inversion of Control
- Service Container
- Service Provider
- Factory Pattern
- Abstract Factory
- Cross-Cutting Concerns
- Aspect-Oriented Programming
- Proxy Pattern
- Decorator Pattern
- POJO / Plain Object
- Plain PHP Class
- Domain Service
- Middleware
- Event / Listener
- Transaction Management
- Logging
- Caching
- Authorization
- Validation
- Delayed Decision
- Big Design Up Front
- Incremental Architecture
- Evolutionary Design
- Standards
- Framework Coupling
- Domain-Specific Language
- Simple Design

---

# Tóm tắt ngắn để đưa vào báo cáo

Chương **Systems** nhấn mạnh rằng một hệ thống sạch không chỉ phụ thuộc vào code ở cấp độ hàm hoặc class, mà còn phụ thuộc vào cách tổ chức kiến trúc tổng thể.

Hệ thống nên tách biệt rõ ràng giữa việc xây dựng object và việc sử dụng object, giữa logic nghiệp vụ và các concern kỹ thuật như logging, bảo mật, transaction, cache.

Các kỹ thuật như Dependency Injection, Factory, Proxy, Decorator, AOP và DSL giúp hệ thống dễ kiểm thử, dễ mở rộng và ít phụ thuộc vào framework.

Tinh thần chính của chương là xây dựng hệ thống đơn giản, linh hoạt, có thể phát triển dần theo nhu cầu thực tế thay vì thiết kế quá phức tạp ngay từ đầu.
