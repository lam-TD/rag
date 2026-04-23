# Checklist Review Code cho task Refactor DI (Dependency Injection)

> Mục tiêu: dùng checklist này để review các pull request/refactor liên quan đến DI, đặc biệt với **Injector** / **fastapi-injector** trong dự án Python/FastAPI.

---

## 1. Mục tiêu review

- [ ] Phần refactor làm rõ dependency của hệ thống thay vì che giấu chúng.
- [ ] Phần refactor giúp code **dễ đọc hơn, dễ test hơn, dễ thay thế implementation hơn**.
- [ ] Phần refactor **không làm thay đổi hành vi nghiệp vụ ngoài mong đợi**.
- [ ] DI chỉ được dùng để quản lý wiring/object graph, **không nhét business logic vào container/module/provider**.

---

## 2. Constructor Injection

- [ ] Dependency chính của class được khai báo rõ trong `__init__`.
- [ ] Không giấu dependency ở trong method khi thực tế nó là dependency cố định của object.
- [ ] Không khởi tạo trực tiếp dependency bằng `ConcreteClass()` bên trong service nếu dependency đó đáng ra phải được inject.
- [ ] Type annotation rõ ràng, nhất quán, giúp người đọc nhìn constructor là hiểu class cần gì.
- [ ] Constructor không nhận quá nhiều dependency bất thường.
- [ ] Nếu constructor có quá nhiều dependency, reviewer đã xem xét:
  - [ ] Class đang ôm quá nhiều trách nhiệm.
  - [ ] Có thể tách service/use case nhỏ hơn.
  - [ ] Có dependency nào là “helper phụ” nhưng đang bị đẩy vào sai tầng hay không.

**Câu hỏi review gợi ý**
- Class này có đang phụ thuộc vào đúng những gì nó thực sự cần không?
- Có dependency nào đang bị ẩn trong code thay vì xuất hiện ở constructor không?

---

## 3. Không dùng Service Locator trá hình

- [ ] Không inject cả `Injector` vào service chỉ để gọi `injector.get(...)`.
- [ ] Không dùng container như một global lookup mechanism.
- [ ] Code nghiệp vụ không phụ thuộc trực tiếp vào container.
- [ ] Việc resolve object tập trung ở composition root / wiring layer, không rải rác khắp hệ thống.

**Dấu hiệu xấu**
- `self.injector.get(...)` xuất hiện trong service nghiệp vụ.
- Một class chỉ nhận `Injector` thay vì nhận dependency thật.
- Route/service/job tự đi lấy dependency từ container thay vì được cấp sẵn.

---

## 4. Module / Binding / Provider

- [ ] Binding được đặt ở nơi hợp lý, dễ tìm, dễ đọc.
- [ ] Tên module phản ánh đúng mục đích (`AppModule`, `InfraModule`, `RepositoryModule`...).
- [ ] Không bind trùng lặp khó hiểu giữa nhiều module.
- [ ] Không có binding “thừa” không còn được dùng.
- [ ] Không có provider chứa business logic.
- [ ] Provider chỉ làm nhiệm vụ tạo object/wiring.
- [ ] Provider không làm I/O nặng, không gọi mạng lâu, không thực hiện xử lý blocking phức tạp.
- [ ] Nếu object cần cấu hình đặc biệt, reviewer kiểm tra provider có thật sự cần thiết hay chỉ đang che giấu logic không nên đặt ở đó.

**Câu hỏi review gợi ý**
- Logic trong provider có đang vượt quá trách nhiệm “khởi tạo object” không?
- Nếu bỏ DI đi, logic này có còn nên tồn tại ở đây không?

---

## 5. Scope / Lifecycle

- [ ] Scope của từng dependency được chọn có chủ đích, không chọn theo cảm tính.
- [ ] Dependency dùng chung toàn app mới để `singleton`.
- [ ] Dependency mang state theo request không bị bind thành singleton nhầm.
- [ ] Resource theo request/job/background được quản lý vòng đời đúng cách.
- [ ] Không có dấu hiệu rò rỉ state giữa các request.
- [ ] Nếu dùng `fastapi-injector` request scope:
  - [ ] Middleware/scope setup đã đúng.
  - [ ] Cleanup đã được bật hoặc được xử lý rõ ràng.
- [ ] Với background job / scheduler / worker:
  - [ ] Reviewer đã kiểm tra scope ngoài HTTP request.
  - [ ] Không tái sử dụng request-scoped object sai ngữ cảnh.
  - [ ] Có chiến lược tạo scope riêng nếu cần.

**Các lỗi thường gặp**
- Gắn `singleton` cho object có dữ liệu theo request.
- Dùng cùng một object DB session cho nhiều request/job.
- Dùng dependency request-scope trong APScheduler/aio-pika worker mà không có scope phù hợp.

---

## 6. FastAPI integration

- [ ] Route handler không tự khởi tạo service bằng tay nếu service đó đã thuộc DI graph.
- [ ] Wiring giữa FastAPI và Injector rõ ràng, nhất quán trong toàn dự án.
- [ ] Không trộn quá nhiều kiểu inject khác nhau gây khó hiểu cho team.
- [ ] Middleware, exception handler, background task có cách lấy dependency nhất quán.
- [ ] Những dependency đặc biệt của FastAPI (`Request`, `Response`, `BackgroundTasks`, ...) được xử lý đúng tầng, không ép nhét sai vào domain/service nếu không cần.

**Câu hỏi review gợi ý**
- Có chỗ nào route chỉ đang đóng vai trò “composition root mini” một cách không cần thiết không?
- Có chỗ nào phụ thuộc framework bị chảy sâu vào tầng service/domain không?

---

## 7. Ranh giới giữa abstraction và implementation

- [ ] Service phụ thuộc vào abstraction khi điều đó mang lại lợi ích thực sự.
- [ ] Không lạm dụng interface/protocol cho mọi thứ một cách máy móc.
- [ ] Nếu chỉ có một implementation và chưa có nhu cầu thay thế, reviewer đánh giá xem abstraction hiện tại có hợp lý không.
- [ ] Các abstraction đang phản ánh nhu cầu của application, không phản ánh máy móc theo thư viện/framework.

**Dấu hiệu tốt**
- Dễ thay repo/client/fake trong test.
- Service không biết quá nhiều về chi tiết kỹ thuật của implementation cụ thể.

---

## 8. Quản lý cấu hình và resource

- [ ] Config được inject rõ ràng, không đọc env rải rác trong code nghiệp vụ.
- [ ] Không truyền nguyên khối config quá lớn vào class nếu class chỉ cần một phần nhỏ.
- [ ] Các resource như `httpx.AsyncClient`, DB connection/session, producer/consumer... có vòng đời rõ ràng.
- [ ] Reviewer đã kiểm tra việc close/cleanup resource.
- [ ] Không khởi tạo resource đắt đỏ lặp đi lặp lại nếu đáng ra nên reuse.

**Câu hỏi review gợi ý**
- Class này thực sự cần toàn bộ config hay chỉ cần 1-2 giá trị?
- Resource này nên là singleton, request scope hay factory ngắn hạn?

---

## 9. Testability

- [ ] Sau refactor, class/service có dễ unit test hơn trước.
- [ ] Có thể thay dependency thật bằng fake/mock/stub một cách rõ ràng.
- [ ] Không cần patch quá sâu chỉ để test business logic.
- [ ] Test không phụ thuộc ngầm vào global state/container state.
- [ ] Có test cho wiring quan trọng nếu refactor chạm vào module/binding/scope.
- [ ] Nếu scope/lifecycle thay đổi, reviewer đã xem có cần bổ sung integration test hay không.

**Dấu hiệu tốt**
- Có thể khởi tạo service trong test bằng fake dependency đơn giản.
- Test business logic không cần boot cả app/container nếu không cần.

---

## 10. Độ rõ ràng và khả năng bảo trì

- [ ] Cấu trúc file/module DI dễ lần theo.
- [ ] Tên class/tên provider/tên module rõ ràng.
- [ ] Người mới vào dự án có thể xác định “dependency này được bind ở đâu” trong thời gian ngắn.
- [ ] Refactor không làm team phải học thêm pattern phức tạp không cần thiết.
- [ ] Nếu có custom scope/custom helper, code đã có comment hoặc tài liệu giải thích.
- [ ] PR có nêu rõ lý do refactor và trade-off.

---

## 11. Anti-pattern cần bắt trong review

- [ ] Inject `Injector` vào service nghiệp vụ.
- [ ] Provider làm việc nặng, gọi API, truy vấn DB phức tạp, hoặc chứa business rule.
- [ ] Singleton hóa bừa bãi.
- [ ] Dependency theo request nhưng lại được cache/global hóa.
- [ ] Route/service tự `new` implementation cụ thể trong nhiều nơi.
- [ ] Abstraction quá mức cho các thành phần chưa có nhu cầu thay thế.
- [ ] Một class nhận quá nhiều dependency do đang ôm quá nhiều trách nhiệm.
- [ ] Refactor DI nhưng thực tế chỉ di chuyển code, không cải thiện coupling/cohesion.
- [ ] Code chỉ “đúng với DI framework” nhưng lại khó đọc hơn với người bảo trì.

---

## 12. Checklist quyết định cuối cùng

### Có thể approve khi:
- [ ] Dependency rõ ràng hơn trước.
- [ ] Scope/lifecycle hợp lý và an toàn.
- [ ] Wiring dễ hiểu, không lạm dụng container.
- [ ] Testability được cải thiện hoặc ít nhất không tệ đi.
- [ ] Refactor làm giảm coupling hoặc tăng khả năng thay thế dependency.
- [ ] Không xuất hiện anti-pattern nghiêm trọng.

### Cần yêu cầu chỉnh sửa khi:
- [ ] Có dấu hiệu service locator.
- [ ] Scope chưa rõ hoặc có nguy cơ rò rỉ state.
- [ ] Provider đang chứa logic không phù hợp.
- [ ] Code khó test hơn sau refactor.
- [ ] Refactor làm cấu trúc phức tạp hơn nhưng không đem lại lợi ích rõ ràng.

---

## 13. Mẫu comment review ngắn có thể dùng trực tiếp

### Khi dependency đang bị ẩn
> Dependency này có vẻ là phụ thuộc cố định của class, nên cân nhắc đưa lên constructor để làm rõ contract của object.

### Khi đang dùng service locator
> Chỗ này đang có xu hướng service locator vì class nhận `Injector` rồi tự `get()` dependency. Nên inject trực tiếp dependency cần dùng để code rõ ràng và dễ test hơn.

### Khi scope chưa an toàn
> Chỗ binding này cần làm rõ lifecycle. Nếu object mang state theo request/job thì việc để singleton có thể gây leak state hoặc dùng sai context.

### Khi provider làm quá nhiều việc
> Provider này đang vượt quá trách nhiệm wiring/khởi tạo object. Nên tách phần business logic hoặc I/O nặng ra khỏi provider để dễ hiểu và an toàn hơn.

### Khi abstraction chưa hợp lý
> Chỗ này có thể đang trừu tượng hóa hơi sớm. Nếu hiện tại chưa có nhu cầu thay implementation, mình nên cân nhắc giữ đơn giản để giảm độ phức tạp.

---

## 14. Gợi ý cách dùng checklist trong team

- [ ] Review theo thứ tự: **dependency clarity -> scope -> provider -> testability -> anti-pattern**.
- [ ] Với PR nhỏ: chỉ cần check các mục cốt lõi.
- [ ] Với PR refactor lớn: nên review thêm sơ đồ wiring hoặc mô tả object graph.
- [ ] Nếu task liên quan FastAPI + background job + scheduler, bắt buộc review riêng phần scope ngoài request.
- [ ] Nếu refactor chạm vào resource quan trọng (DB, HTTP client, MQ), cần kiểm tra lifecycle và cleanup kỹ hơn.

---

## 15. Kết luận ngắn

Refactor DI được xem là tốt khi nó giúp hệ thống:

- [ ] **rõ dependency hơn**
- [ ] **ít coupling hơn**
- [ ] **dễ test hơn**
- [ ] **quản lý lifecycle an toàn hơn**
- [ ] **không lạm dụng DI framework**

Nếu một refactor chỉ làm tăng số lớp, tăng số module, tăng độ “ảo thuật”, nhưng không cải thiện các điểm trên, thì đó chưa phải là refactor DI tốt.
