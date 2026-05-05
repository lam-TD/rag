Chương 6 của cuốn sách có tiêu đề **"Objects and Data Structures"** (Đối tượng và Cấu trúc dữ liệu), tập trung vào việc phân biệt giữa hai khái niệm này và cách sử dụng chúng hiệu quả để giữ cho mã nguồn linh hoạt [1]. Dưới đây là tóm tắt các nội dung chính:

### 1. Trừu tượng hóa dữ liệu (Data Abstraction)
Việc ẩn đi các chi tiết thực thi không chỉ đơn thuần là đặt một lớp hàm (getters/setters) giữa các biến [2]. 
*   **Bản chất:** Một lớp không nên chỉ đẩy các biến của nó ra ngoài qua các hàm truy cập, mà nên **phơi bày các giao diện trừu tượng** cho phép người dùng thao tác trên "bản chất" của dữ liệu mà không cần biết cách nó được thực hiện bên dưới [2, 3].
*   **Quy tắc:** Chúng ta muốn thể hiện dữ liệu dưới dạng các thuật ngữ trừu tượng thay vì các chi tiết cụ thể [3].

### 2. Sự bất đối xứng giữa Đối tượng và Cấu trúc dữ liệu (Data/Object Anti-Symmetry)
Đây là sự khác biệt cốt lõi ảnh hưởng đến thiết kế hệ thống [4]:
*   **Đối tượng (Objects):** Ẩn dữ liệu sau các trừu tượng và phơi bày các hàm thao tác trên dữ liệu đó [4].
    *   **Ưu điểm:** Dễ dàng thêm các loại đối tượng mới mà không cần thay đổi các hàm hiện có [5].
    *   **Nhược điểm:** Khó thêm các hàm mới vì tất cả các lớp phải được thay đổi [5].
*   **Cấu trúc dữ liệu (Data Structures):** Phơi bày dữ liệu và không có các hàm mang ý nghĩa nghiệp vụ [4].
    *   **Ưu điểm:** Dễ dàng thêm các hàm mới mà không cần thay đổi cấu trúc dữ liệu hiện có [5].
    *   **Nhược điểm:** Khó thêm cấu trúc dữ liệu mới vì tất cả các hàm hiện tại đều phải thay đổi [5].

Tác giả nhấn mạnh rằng các lập trình viên trưởng thành sẽ hiểu rằng không phải mọi thứ đều là đối tượng; đôi khi các cấu trúc dữ liệu đơn giản kết hợp với các thủ tục lại là lựa chọn phù hợp hơn cho bài toán cụ thể [6].

### 3. Định luật Demeter (The Law of Demeter)
Định luật này cho rằng một module không nên biết về các chi tiết bên trong của các đối tượng mà nó thao tác [7].
*   **Quy tắc:** Một phương thức *f* của lớp *C* chỉ nên gọi các phương thức của: bản thân *C*, đối tượng được tạo bởi *f*, đối tượng được truyền vào làm đối số cho *f*, hoặc đối tượng nằm trong biến thực thể của *C* [7, 8].
*   **Tránh "Vụ tai nạn tàu hỏa" (Train Wrecks):** Các chuỗi gọi hàm liên tiếp như `ctxt.getOptions().getScratchDir().getAbsolutePath()` được coi là phong cách mã nguồn cẩu thả và nên tránh [9]. Nếu đó là các đối tượng có hành vi thực sự, chúng nên ẩn đi cấu trúc bên trong và chúng ta nên yêu cầu chúng thực hiện một hành động nào đó (Tell, don't ask) [10].

### 4. DTO và Active Record
*   **Data Transfer Object (DTO):** Là dạng tinh túy của cấu trúc dữ liệu — một lớp có các biến công khai và không có hàm [11]. Chúng rất hữu ích khi giao tiếp với cơ sở dữ liệu hoặc phân giải các thông báo từ socket [11].
*   **Active Record:** Một dạng đặc biệt của DTO, ngoài các biến còn có các phương thức điều hướng như `save` và `find` [12]. Sai lầm phổ biến là đưa các phương thức quy tắc nghiệp vụ vào Active Record, biến chúng thành một "thực thể lai" (hybrid) — vừa là đối tượng vừa là cấu trúc dữ liệu [12, 13]. Tác giả khuyên nên coi Active Record là cấu trúc dữ liệu và tạo ra các đối tượng riêng biệt chứa các quy tắc nghiệp vụ [13].

**Kết luận:** Đối tượng phơi bày hành vi và ẩn dữ liệu, giúp dễ thêm loại đối tượng mới nhưng khó thêm hành vi mới [13]. Cấu trúc dữ liệu phơi bày dữ liệu và không có hành vi, giúp dễ thêm hành vi mới nhưng khó thêm cấu trúc mới [13]. Người lập trình giỏi sẽ chọn cách tiếp cận tốt nhất cho từng công việc cụ thể mà không có định kiến [14].