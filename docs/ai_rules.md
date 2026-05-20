# Kế hoạch Triển khai AI vào Workflow Phát triển (Thử nghiệm 3 tháng)

## 1. Bối cảnh và Lý do thực hiện

Trong bối cảnh các công cụ AI hỗ trợ lập trình đang phát triển nhanh và được nhiều đội phát triển phần mềm áp dụng, nhóm cần đánh giá một cách có hệ thống xem việc tích hợp AI vào quy trình làm việc hàng ngày có thực sự mang lại lợi ích hay không, lợi ích đó lớn đến mức nào, và đi kèm với những đánh đổi gì. Việc đưa ra quyết định triển khai chính thức mà không qua giai đoạn thử nghiệm có kiểm soát sẽ tiềm ẩn rủi ro về chất lượng code, bảo mật, và sự xáo trộn không cần thiết trong workflow đã ổn định của nhóm.

Dự án thử nghiệm này được thiết kế kéo dài ba tháng, đủ dài để vượt qua giai đoạn “honeymoon” khi mọi người còn hào hứng với công cụ mới, đồng thời đủ ngắn để không tiêu tốn quá nhiều nguồn lực nếu kết quả không như kỳ vọng. Kết thúc dự án, nhóm sẽ có cơ sở dữ liệu định lượng và định tính để đưa ra quyết định triển khai chính thức, mở rộng phạm vi, hoặc dừng lại.

## 2. Mục tiêu

### 2.1. Mục tiêu chính

Đánh giá hiệu suất làm việc của nhóm khi có sự hỗ trợ của AI thông qua hai trục đo lường là tốc độ hoàn thành công việc và chất lượng output. Hai trục này được chọn vì chúng phản ánh trực tiếp giá trị mà AI có thể mang lại hoặc làm tổn hại, và đều có thể đo lường được bằng các công cụ sẵn có trong quy trình hiện tại.

### 2.2. Mục tiêu phụ

Đúc kết và ghi chép lại kinh nghiệm sử dụng AI một cách có hệ thống để xây dựng “bộ nhớ tập thể” của nhóm. Đây là tài sản quan trọng vì khác với một công cụ truyền thống chỉ cần học cách dùng một lần, AI đòi hỏi kỹ năng prompt và phán đoán liên tục phát triển. Nếu kinh nghiệm chỉ nằm trong đầu từng cá nhân, nhóm sẽ phải học lại từ đầu mỗi khi có thành viên mới.

## 3. Tool và Cấu hình

### 3.1. Giới thiệu công cụ

Nhóm sẽ sử dụng Cline tích hợp trong VS Code làm công cụ AI chính. Cline là một extension biến VS Code thành môi trường làm việc với AI agent, cho phép AI không chỉ gợi ý code mà còn đọc file, chạy lệnh terminal, sửa file trực tiếp, và thực hiện các chuỗi thao tác phức tạp. Đây là sự khác biệt quan trọng so với các công cụ chỉ đơn thuần sinh code, vì nó cho phép AI tham gia vào toàn bộ vòng đời của một task chứ không chỉ giai đoạn viết code.

### 3.2. Cấu hình kỹ thuật

Cấu hình kỹ thuật là lớp đầu tiên cần thống nhất trong toàn nhóm để đảm bảo mọi người làm việc trên cùng một nền tảng. Khi mỗi người dùng một model khác nhau hoặc một cách cấu hình khác nhau, dữ liệu thu được sẽ không thể so sánh được, làm hỏng mục tiêu đo lường của dự án.

Về phiên bản, nhóm sẽ thống nhất sử dụng cùng một phiên bản VS Code và Cline, được chốt vào tuần 1 và chỉ cập nhật khi có quyết định chung. Việc này tránh tình trạng một thành viên gặp bug do phiên bản cũ trong khi người khác không gặp, gây nhầm lẫn khi đánh giá.

Về model AI, nhóm cần chọn một model chính làm chuẩn cho toàn dự án. Mỗi model có đặc tính khác nhau về tốc độ, chi phí, và chất lượng, nên việc chốt model giúp loại bỏ một biến số khi so sánh hiệu suất giữa các thành viên. Trong trường hợp cần thử nghiệm model khác, thành viên cần ghi chú rõ trong log để tách bạch khi phân tích dữ liệu.

Về quyền truy cập tự động, Cline cho phép AI tự động chạy lệnh và sửa file mà không cần xác nhận từng bước. Trong giai đoạn đầu của dự án, nhóm nên đặt chế độ yêu cầu xác nhận cho mọi thao tác ghi file và chạy lệnh, đến khi thành viên đủ tự tin với hành vi của AI mới mở rộng quyền tự động. Đây là biện pháp phòng vệ tránh AI vô tình xóa hoặc sửa nhầm code quan trọng.

Về biến môi trường, nhóm cần thiết lập file `.env` riêng cho từng thành viên chứa API key, và đảm bảo file này được thêm vào `.gitignore` của cả dự án thử nghiệm lẫn các repo công việc. Đây là phòng tuyến đầu tiên chống rò rỉ credential.

### 3.3. Cấu hình ngữ cảnh dự án

Cấu hình ngữ cảnh là lớp thứ hai, quan trọng hơn cấu hình kỹ thuật vì nó quyết định chất lượng output của AI. AI không có hiểu biết sẵn về codebase, quy ước nội bộ, hoặc kiến trúc dự án của nhóm, nên cần được cung cấp thông tin này một cách tường minh.

Mỗi repo tham gia thử nghiệm sẽ có một file `.clinerules` đặt ở thư mục gốc, đóng vai trò như “sổ tay onboarding” cho AI. File này chứa các thông tin nền tảng mà AI cần biết trước khi làm bất kỳ task nào trong repo, bao gồm kiến trúc tổng quan, các package chính và mục đích của chúng, quy ước đặt tên biến và file, phong cách code mà nhóm theo, danh sách thư viện cấm sử dụng vì lý do bảo mật hoặc license, và các pattern đặc thù của dự án mà AI cần tuân thủ.

Việc xây dựng file `.clinerules` là một khoản đầu tư ban đầu cần khoảng nửa ngày đến một ngày làm việc của lead developer, nhưng nó sẽ tiết kiệm hàng giờ về sau vì AI không cần được nhắc đi nhắc lại các quy ước này trong mỗi prompt. Hãy hình dung nó giống như tài liệu chào đón nhân viên mới, viết một lần dùng cho nhiều người.

### 3.4. Cấu hình tổ chức

Cấu hình tổ chức là các quy ước về cách cả nhóm cùng làm việc với AI, không phải các thiết lập kỹ thuật. Đây là lớp dễ bị quên nhưng lại quyết định tính nhất quán của dữ liệu thu thập được.

Nhóm cần thống nhất quy ước về việc gắn nhãn commit và pull request có sử dụng AI. Một cách đơn giản là thêm prefix `[AI]` hoặc trailer `AI-Assisted: yes` vào commit message khi code được AI sinh ra phần lớn. Quy ước này giúp việc phân tích sau ba tháng trở nên dễ dàng vì có thể tách bạch code AI và code thuần để so sánh tỷ lệ bug.

Nhóm cũng cần thống nhất về phạm vi được phép giao cho AI làm việc. Ví dụ, các file chứa logic xử lý thanh toán, xác thực, hoặc mật mã có thể được đánh dấu là “AI read-only” tức là AI chỉ được đọc để hiểu ngữ cảnh chứ không được tự sửa. Quy ước này nên được liệt kê trong file `.clinerules` để AI tự biết và tuân thủ.

## 4. Cách triển khai

### 4.1. Triết lý nền tảng

Cách tiếp cận của dự án dựa trên một nguyên tắc quan trọng. AI không phải là một con người có khả năng suy luận toàn diện về bối cảnh công việc, mà là một công cụ mạnh khi được giao đúng việc với đúng thông tin. Vì vậy, thay vì hỏi “AI có thể làm task này không”, nhóm sẽ luôn hỏi “task này gồm những bước nhỏ nào, AI hỗ trợ bước nào tốt nhất, và mỗi bước cần chuẩn bị gì để AI làm được tốt”.

Cách đặt câu hỏi này dẫn đến một quy trình bốn bước được áp dụng cho mọi loại nhiệm vụ trong dự án, sẽ được mô tả ở mục 4.2 ngay sau đây.

### 4.2. Quy trình bốn bước

Bước thứ nhất là chia nhỏ nhiệm vụ thành các bước logic. Trước khi đụng đến AI, thành viên cần ngồi xuống và liệt kê các bước cần làm để hoàn thành nhiệm vụ, giống như khi viết task list cho một đồng nghiệp mới. Việc này có lợi ích kép. Lợi ích thứ nhất là tự nó đã giúp người làm hiểu rõ task hơn, dù có dùng AI hay không. Lợi ích thứ hai là tạo ra cấu trúc rõ ràng để quyết định bước nào giao cho AI, bước nào tự làm.

Bước thứ hai là phân loại từng bước theo mức độ phù hợp với AI. Có ba nhóm chính. Nhóm “AI làm chủ đạo” là các bước có đầu vào đầu ra rõ ràng, có thể kiểm tra được kết quả, ít rủi ro nếu sai. Ví dụ như viết unit test cho một function đã có, tạo boilerplate code, viết docstring, refactor đổi tên biến. Nhóm “AI hỗ trợ, người quyết định” là các bước cần phán đoán nhưng AI có thể đưa ra gợi ý hữu ích. Ví dụ như thiết kế cấu trúc cho một module mới, chọn thư viện, viết logic nghiệp vụ phức tạp. Nhóm “người làm chủ đạo” là các bước cần hiểu biết sâu về bối cảnh hoặc có rủi ro cao. Ví dụ như quyết định kiến trúc tổng thể, xử lý dữ liệu nhạy cảm, đánh giá tác động bảo mật.

Bước thứ ba là chuẩn bị ngữ cảnh cho AI ở các bước mà AI tham gia. Đây là bước quyết định chất lượng output. Ngữ cảnh cần chuẩn bị bao gồm mô tả rõ ràng về task, các file liên quan mà AI cần đọc, các ràng buộc cụ thể như phải dùng thư viện nào hoặc không được dùng pattern nào, ví dụ về output mong muốn nếu có, và tiêu chí thành công để AI biết khi nào thì xong. Một mẹo thực tế là viết prompt dưới dạng instruction cho một junior developer mới vào nhóm, vì cả hai đều thiếu ngữ cảnh và cần được hướng dẫn cụ thể.

Bước thứ tư là thực thi và kiểm tra. Thành viên giao task cho AI thực hiện, sau đó review output với cùng tiêu chuẩn như khi review code của đồng nghiệp. Nếu output không đạt, thay vì sửa thủ công, hãy quay lại bước ba để cải thiện ngữ cảnh và prompt, vì đây là kinh nghiệm quý giá cho cả nhóm. Mọi prompt thành công và thất bại đều được ghi lại theo cơ chế ở mục 6 để tích lũy kinh nghiệm.

### 4.3. Mức độ tự chủ của AI

Trong dự án thử nghiệm, nhóm sẽ thử nghiệm ba mức độ tự chủ khác nhau và ghi nhận mức nào phù hợp với loại task nào.

Mức một là “AI gợi ý, người làm”. AI đưa ra đề xuất, thành viên đọc và tự gõ code. Phù hợp với task nhỏ, có rủi ro, hoặc khi thành viên muốn học từ output của AI.

Mức hai là “AI làm, người review từng bước”. AI thực hiện thao tác nhưng phải xác nhận trước mỗi lần ghi file hoặc chạy lệnh. Phù hợp với task vừa, ngữ cảnh đã rõ ràng nhưng vẫn cần kiểm soát.

Mức ba là “AI tự chủ, người review kết quả cuối”. AI thực hiện toàn bộ chuỗi thao tác và chỉ báo lại khi hoàn thành. Phù hợp với task có đầu ra dễ kiểm chứng như viết test, hoặc task lặp đi lặp lại đã được chứng minh là AI làm tốt.

Việc thử nghiệm cả ba mức độ giúp nhóm tìm ra “ngưỡng tự chủ” phù hợp với từng loại công việc, thay vì chọn một mức cố định cho tất cả.

## 5. Các nhiệm vụ sẽ triển khai

### 5.1. Nhiệm vụ 1 - Điều tra CVE

Đây là nhiệm vụ định kỳ của nhóm với mục tiêu kép là đánh giá mức độ ảnh hưởng của lỗ hổng đến sản phẩm và sau đó vá lỗ hổng nếu cần. Hai mục tiêu này có tính chất rất khác nhau nên cần được tách thành các giai đoạn riêng trong quy trình.

#### 5.1.1. Phân rã quy trình

Quy trình điều tra một CVE bao gồm sáu bước. Bước một là tiếp nhận thông tin CVE, đọc mô tả lỗ hổng, package bị ảnh hưởng, phiên bản bị ảnh hưởng, và CVSS score. Bước hai là kiểm tra dependency, xác định xem codebase có thực sự dùng package bị ảnh hưởng không, ở phiên bản nào, là dependency trực tiếp hay gián tiếp. Bước ba là phân tích cách sử dụng, tìm tất cả các vị trí trong codebase đang dùng package này và xem có dùng đúng phần dễ tổn thương hay không. Bước bốn là đánh giá mức độ ảnh hưởng thực tế, dựa trên ngữ cảnh sử dụng và bối cảnh triển khai để quyết định lỗ hổng có thực sự đe dọa sản phẩm hay không. Bước năm là viết báo cáo đánh giá. Bước sáu là viết patch nếu kết luận cần fix.

#### 5.1.2. AI hỗ trợ ở bước nào

Bước một là việc thuần đọc và tóm tắt, AI làm rất tốt. Có thể yêu cầu AI đọc bản tin CVE và trích xuất các thông tin then chốt vào một format chuẩn để dễ xử lý các bước sau.

Bước hai có thể kết hợp công cụ tự động và AI. Với codebase Python, công cụ như `pip-audit` hoặc `safety` đã có thể quét tự động dependency tree và so khớp với CVE database. AI có thể hỗ trợ giải thích kết quả quét và truy ngược về `requirements.txt` hoặc `pyproject.toml` để hiểu tại sao một package gián tiếp lại có mặt.

Bước ba là điểm AI đặc biệt mạnh. AI có thể grep toàn bộ codebase tìm import của package bị ảnh hưởng, sau đó đọc từng vị trí sử dụng và so sánh với mô tả lỗ hổng để xác định có dùng đúng phần dễ tổn thương không. Ví dụ nếu CVE chỉ ảnh hưởng một function cụ thể của package, AI có thể nhanh chóng kiểm tra xem code có gọi đúng function đó không.

Bước bốn là bước người làm chủ đạo. Đánh giá ảnh hưởng thực tế cần hiểu biết về kiến trúc deploy, dữ liệu nhạy cảm nào đang được xử lý, lỗ hổng có thể bị khai thác trong bối cảnh cụ thể của sản phẩm hay không. AI có thể đưa ra gợi ý nhưng quyết định cuối cùng thuộc về con người, vì đánh giá sai ở bước này có thể dẫn đến bỏ qua lỗ hổng nguy hiểm hoặc lãng phí nguồn lực fix lỗ hổng không quan trọng.

Bước năm là việc viết văn bản có cấu trúc, AI làm tốt. Có thể yêu cầu AI tổng hợp các phát hiện từ bước một đến bước bốn thành báo cáo theo template chuẩn của nhóm.

Bước sáu là phần phức tạp nhất và cần workflow riêng giống như quá trình code, sẽ được mô tả ở mục 5.2.

#### 5.1.3. Chuẩn bị cho AI

Để AI hỗ trợ hiệu quả nhiệm vụ này, nhóm cần chuẩn bị ba thứ. Thứ nhất là template báo cáo CVE chuẩn, lưu trong repo dự án, để AI biết format đầu ra mong muốn. Thứ hai là một prompt mẫu cho từng bước trong quy trình, được lưu trong prompt library. Thứ ba là một file ngữ cảnh bảo mật riêng cho mỗi repo, mô tả tóm tắt cách sản phẩm được triển khai, loại dữ liệu xử lý, và surface tấn công, để AI có cơ sở khi đánh giá ảnh hưởng ở bước ba và gợi ý ở bước bốn.

#### 5.1.4. Ví dụ workflow thực tế

Giả sử nhóm nhận thông báo về CVE-2024-XXXXX ảnh hưởng đến `requests` ở phiên bản dưới 2.32.0. Quy trình áp dụng AI sẽ diễn ra như sau. Mở Cline trong VS Code, yêu cầu AI đọc bản tin CVE và điền vào template báo cáo các thông tin cơ bản. Yêu cầu AI chạy `pip-audit` hoặc kiểm tra file lock để xác định phiên bản `requests` hiện tại. Yêu cầu AI grep toàn bộ codebase tìm các vị trí dùng `requests` và phân loại theo cách sử dụng. Người làm đọc kết quả AI tổng hợp, kết hợp với hiểu biết về sản phẩm để quyết định mức độ ưu tiên fix. Yêu cầu AI viết draft báo cáo đánh giá dựa trên các phát hiện. Nếu quyết định fix, chuyển sang quy trình ở mục 5.2.

### 5.2. Nhiệm vụ 2 - Quá trình code

Quá trình code bao gồm việc viết feature mới, sửa bug, refactor, và viết test. Đây là loại nhiệm vụ đa dạng nhất và là nơi AI có tiềm năng tác động lớn nhất đến hiệu suất. Vì tính đa dạng này, thay vì mô tả một quy trình duy nhất, mục này mô tả khung quy trình chung và các biến thể theo loại task.

#### 5.2.1. Khung quy trình chung

Mọi task code đều đi qua năm giai đoạn. Giai đoạn hiểu yêu cầu, đọc spec hoặc ticket để biết cần làm gì. Giai đoạn khảo sát, đọc codebase liên quan để hiểu phải sửa ở đâu và sửa cái gì. Giai đoạn thiết kế, quyết định cấu trúc của giải pháp. Giai đoạn viết code, biến thiết kế thành code chạy được. Giai đoạn kiểm thử, viết test và chạy thử để xác nhận code hoạt động đúng.

#### 5.2.2. AI hỗ trợ ở giai đoạn nào

Giai đoạn hiểu yêu cầu thường do người làm chủ đạo vì cần đặt câu hỏi với product owner hoặc đồng nghiệp. AI có thể hỗ trợ bằng cách đọc spec và liệt kê các câu hỏi cần làm rõ, hoặc tóm tắt các ticket liên quan đã xử lý trước đây.

Giai đoạn khảo sát là điểm mạnh của AI khi được tích hợp vào VS Code qua Cline. AI có thể đọc nhiều file cùng lúc, tìm các vị trí gọi function, vẽ ra sơ đồ phụ thuộc giữa các module. Với codebase Python, AI có thể truy vết qua các import, decorator, và metaclass mà nếu làm thủ công sẽ tốn rất nhiều thời gian.

Giai đoạn thiết kế nên là phối hợp giữa người và AI. Người đưa ra ý tưởng và ràng buộc, AI đề xuất các phương án và chỉ ra trade-off của từng phương án. Quyết định cuối cùng thuộc về người vì cần cân nhắc yếu tố không có trong code như roadmap sản phẩm, năng lực của nhóm, hoặc deadline.

Giai đoạn viết code là nơi AI có thể làm chủ đạo cho các phần boilerplate, có pattern rõ ràng, hoặc đã có ví dụ tương tự trong codebase. Với Python, AI làm tốt việc viết các class data, các Pydantic model, các function utility, các adapter cho thư viện ngoài. AI cần được người kiểm soát chặt hơn ở các phần chứa logic nghiệp vụ phức tạp, các phần tối ưu hiệu năng, hoặc các phần dùng tính năng Python ít phổ biến như metaclass hay descriptor.

Giai đoạn kiểm thử là một trong những điểm mạnh nhất của AI. Khi đã có code, AI có thể tự sinh ra bộ test bao phủ các case bình thường, case biên, và case lỗi. Tuy nhiên cần lưu ý hai điều. Thứ nhất, AI có xu hướng viết test “trùng khớp với code” thay vì “trùng khớp với yêu cầu”, tức là nếu code có bug thì test cũng sẽ có bug tương ứng. Vì vậy người viết cần xem lại test có thực sự kiểm tra đúng hành vi mong muốn không. Thứ hai, AI có thể tạo ra rất nhiều test trông có vẻ phong phú nhưng thực ra chỉ là biến thể của cùng một case, gây phình to test suite mà không tăng coverage thực sự.

#### 5.2.3. Chuẩn bị cho AI

Để AI hỗ trợ quá trình code hiệu quả, ngoài file `.clinerules` đã đề cập, nhóm cần chuẩn bị thêm các tài liệu sau. Một file mô tả kiến trúc chính, vẽ ra các layer của ứng dụng và quy ước về nơi đặt code mới. Các ví dụ về code chuẩn cho từng loại task phổ biến, ví dụ “đây là cách nhóm viết một API endpoint”, “đây là cách nhóm viết một background job”. Cấu hình linter và formatter như `ruff`, `black`, `mypy` đặt ở thư mục gốc để AI tự áp dụng đúng style. Một file mô tả các pattern bị cấm hoặc không khuyến khích trong codebase, để AI không gợi ý sai.

#### 5.2.4. Ví dụ workflow thực tế

Giả sử có ticket “Thêm endpoint API trả về thống kê đơn hàng theo tháng”. Quy trình áp dụng AI sẽ diễn ra như sau. Đọc ticket, yêu cầu AI tóm tắt và liệt kê thông tin còn thiếu. Sau khi làm rõ với PO, yêu cầu AI khảo sát codebase tìm các endpoint thống kê tương tự đã có để học pattern. Cùng AI thảo luận thiết kế, xác định cần tạo những file nào, dùng query database ra sao. Giao AI viết code endpoint theo pattern đã chốt, người review từng phần thay đổi. Giao AI viết test cho endpoint, người đọc test xem có đúng hành vi mong muốn không. Chạy linter và test, sửa các vấn đề phát sinh.

#### 5.2.5. Workflow cho fix bug

Fix bug có biến thể riêng so với feature mới. Giai đoạn khảo sát quan trọng hơn vì cần tìm nguyên nhân gốc trước khi sửa. AI rất mạnh ở bước này, có thể đọc traceback, tìm function liên quan, và đề xuất giả thuyết nguyên nhân. Tuy nhiên, người làm phải xác minh giả thuyết bằng cách reproduce bug và đọc kỹ logic, không nên tin ngay đề xuất của AI. Một sai lầm thường gặp là AI đưa ra lý giải có vẻ hợp lý nhưng thực ra không phải nguyên nhân thật, dẫn đến fix sai chỗ và bug vẫn còn.

#### 5.2.6. Workflow cho viết patch CVE (nối tiếp 5.1)

Khi đã xác định cần fix một CVE, workflow code sẽ có thêm ràng buộc đặc biệt. Patch cần càng nhỏ càng tốt để giảm rủi ro phát sinh bug mới. Thường chỉ là việc nâng phiên bản package trong `requirements.txt` hoặc `pyproject.toml`. AI có thể hỗ trợ bằng cách kiểm tra changelog của phiên bản mới, liệt kê các breaking change tiềm năng, và quét codebase tìm các vị trí có thể bị ảnh hưởng bởi breaking change đó. Sau khi nâng phiên bản, AI có thể hỗ trợ chạy lại toàn bộ test suite và phân tích các test bị fail. Trong trường hợp không thể nâng phiên bản, AI có thể giúp viết workaround tạm thời ở tầng ứng dụng, ví dụ thêm validation đầu vào để chặn payload gây kích hoạt lỗ hổng.

## 6. Chỉ số đo lường

### 6.1. Thiết lập baseline (Tuần 1)

Trước khi bắt đầu sử dụng AI, nhóm cần ghi nhận các chỉ số hiện tại để có cơ sở so sánh. Đây là bước quan trọng nhất nhưng cũng dễ bị bỏ qua nhất trong các dự án thử nghiệm. Nếu không có baseline, mọi con số sau ba tháng đều trở nên vô nghĩa vì không biết “tốt hơn” hay “tệ hơn” so với cái gì. Baseline sẽ được lấy từ dữ liệu của bốn tuần gần nhất trước khi bắt đầu dự án, dựa trên lịch sử git, ticket tracker, và CI/CD logs.

### 6.2. Nhóm chỉ số về tốc độ

Thời gian hoàn thành trung bình mỗi task được tính từ lúc thành viên bắt đầu làm việc đến lúc task được merge vào branch chính. Cycle time của pull request được tính từ lúc PR được tạo đến lúc được merge, phản ánh cả tốc độ code và tốc độ review. Số lượng task hoàn thành mỗi tuần của cả nhóm, được phân loại theo độ phức tạp để tránh tình trạng tăng số lượng nhưng giảm chất lượng task được chọn làm. Thời gian điều tra trung bình mỗi CVE, từ lúc nhận thông báo đến lúc hoàn tất báo cáo đánh giá, đây là chỉ số riêng cho nhiệm vụ điều tra CVE.

### 6.3. Nhóm chỉ số về chất lượng

Số lượng bug được phát hiện trong giai đoạn QA và sau khi release, tính riêng cho code có sử dụng AI và code không sử dụng AI dựa trên nhãn commit đã quy ước. Tỷ lệ comment trong code review yêu cầu sửa đổi, phản ánh chất lượng code được nộp lên review. Tỷ lệ code do AI sinh ra bị reject hoặc rewrite đáng kể, đây là chỉ số đặc biệt quan trọng vì nó cho biết AI đang thực sự giúp ích hay chỉ tạo thêm việc cho người review. Độ chính xác của đánh giá CVE, đo bằng việc các CVE được đánh giá là không ảnh hưởng có thực sự không gây vấn đề về sau hay không, đây là chỉ số dài hạn cần theo dõi sau dự án.

### 6.4. Cách thu thập

Phần lớn chỉ số có thể tự động hóa thông qua các công cụ sẵn có. Git log và GitHub/GitLab API cung cấp dữ liệu về PR và commit, lọc theo nhãn `[AI]` đã quy ước. Ticket tracker cung cấp dữ liệu về task. Đối với chỉ số khó tự động hóa như “code AI bị reject”, nhóm sẽ duy trì một bảng ghi chép đơn giản, mỗi thành viên cập nhật vào cuối ngày làm việc với template gồm task, mức độ tự chủ của AI, kết quả, và ghi chú.

## 7. Cơ chế đúc kết kinh nghiệm

### 7.1. Prompt library dùng chung

Nhóm sẽ duy trì một repository nội bộ chứa các prompt đã được kiểm chứng là hiệu quả, phân loại theo loại công việc như điều tra CVE, viết test, refactor, debug. Mỗi prompt đi kèm bối cảnh sử dụng và ví dụ về output mà nó tạo ra. Cấu trúc thư mục đề xuất là tách theo nhiệm vụ ở 5.1 và 5.2, mỗi nhiệm vụ có thư mục con cho từng bước trong quy trình.

### 7.2. Log các tình huống đáng chú ý

Bất kỳ thành viên nào gặp tình huống AI làm rất tốt hoặc làm rất tệ đều ghi lại vào một file chung theo template ngắn gồm bối cảnh, prompt đã dùng, kết quả AI trả về, và bài học rút ra. Việc ghi cả tình huống tệ quan trọng không kém tình huống tốt, vì nó giúp cả nhóm tránh được những cái bẫy đã có người vướng phải.

### 7.3. Retrospective định kỳ

Cuối mỗi hai tuần, nhóm dành ba mươi phút để cùng nhau xem lại các tình huống đã log, thảo luận về thay đổi trong workflow, và cập nhật prompt library cùng file `.clinerules`. Tần suất hai tuần được chọn vì đủ dày để giữ momentum nhưng không quá thường xuyên đến mức trở thành gánh nặng.

## 8. Vai trò và Trách nhiệm

Người phụ trách dự án có trách nhiệm theo dõi tiến độ tổng thể, tổng hợp số liệu định kỳ, và là đầu mối giải quyết các vấn đề phát sinh. Lead developer có trách nhiệm xây dựng và duy trì file `.clinerules`, review prompt library trước khi merge. Các thành viên trong nhóm có trách nhiệm sử dụng AI một cách trung thực trong công việc hàng ngày, gắn nhãn commit đúng quy ước, ghi chép kinh nghiệm vào hệ thống chung, và tham gia đầy đủ các buổi retrospective. Quản lý cấp trên có vai trò review báo cáo định kỳ và đưa ra quyết định cuối cùng vào thời điểm kết thúc dự án.

## 9. Timeline và Milestone

Tuần 1 dành cho việc thiết lập baseline, cài đặt công cụ theo cấu hình thống nhất, xây dựng file `.clinerules` ban đầu cho các repo tham gia, và đào tạo nhanh về cách sử dụng Cline. Tuần 2 đến tuần 4 là giai đoạn vận hành ban đầu, nơi nhóm làm quen với việc tích hợp AI vào workflow theo quy trình ở mục 4, sẽ có nhiều biến động trong số liệu nên không nên vội kết luận. Tuần 5 đến tuần 10 là giai đoạn vận hành ổn định, dữ liệu thu được trong giai đoạn này có giá trị tham khảo cao nhất. Tuần 11 là giai đoạn tổng hợp số liệu và viết báo cáo. Tuần 12 là buổi tổng kết và ra quyết định.

## 10. Rủi ro và Biện pháp Xử lý

### 10.1. Rủi ro về bảo mật và lộ thông tin

Khi AI xử lý code, có khả năng thông tin nhạy cảm như API key, mật khẩu, hoặc logic nghiệp vụ bí mật được gửi đến server bên thứ ba. Biện pháp xử lý là thiết lập danh sách các module không được phép sử dụng AI trong file `.clinerules`, kiểm tra cấu hình Cline để hiểu rõ dữ liệu nào được gửi đi đâu, và yêu cầu thành viên không bao giờ paste credentials vào prompt.

### 10.2. Rủi ro về chất lượng code

AI có thể sinh ra code trông có vẻ đúng nhưng chứa lỗi tinh vi, hoặc sử dụng các pattern không phù hợp với codebase. Biện pháp xử lý là yêu cầu mọi code do AI sinh ra đều phải qua review của con người với cùng tiêu chuẩn như code tự viết, và khuyến khích thành viên chạy đầy đủ test trước khi commit.

### 10.3. Rủi ro về đánh giá CVE sai

Đánh giá sai một CVE là không ảnh hưởng trong khi thực ra có ảnh hưởng có thể dẫn đến lỗ hổng tồn tại trong production. Biện pháp xử lý là yêu cầu mọi đánh giá “không ảnh hưởng” cho CVE có CVSS từ 7.0 trở lên phải được hai người độc lập xác nhận, và AI chỉ đóng vai trò gợi ý chứ không quyết định.

### 10.4. Rủi ro về sự phụ thuộc

Thành viên có thể trở nên phụ thuộc vào AI đến mức suy giảm kỹ năng tự giải quyết vấn đề, đặc biệt là các kỹ sư mới. Biện pháp xử lý là duy trì các hoạt động học tập truyền thống như pair programming và code review chi tiết, đồng thời khuyến khích văn hóa hiểu code do AI sinh ra trước khi accept.

### 10.5. Rủi ro về đo lường không trung thực

Khi biết mình đang được đo, thành viên có xu hướng thay đổi hành vi, hiện tượng được gọi là Hawthorne effect. Biện pháp xử lý là nhấn mạnh rằng mục tiêu của dự án là đánh giá công cụ chứ không phải đánh giá cá nhân, và đảm bảo số liệu cá nhân không được dùng cho việc đánh giá hiệu suất nhân viên trong giai đoạn này.

## 11. Tiêu chí Đánh giá Kết thúc Dự án

Dự án được xem là thành công và nên triển khai chính thức nếu sau ba tháng, các chỉ số tốc độ cải thiện rõ rệt mà không kèm theo suy giảm chất lượng, hoặc chất lượng cải thiện mà không kèm suy giảm tốc độ. Dự án cần được điều chỉnh và thử nghiệm tiếp nếu kết quả lẫn lộn, ví dụ tốc độ tăng nhưng chất lượng giảm nhẹ, để tìm cách cải thiện workflow. Dự án nên dừng lại nếu không có cải thiện rõ rệt ở cả hai trục, hoặc nếu xuất hiện rủi ro nghiêm trọng về bảo mật hoặc chất lượng trong quá trình thử nghiệm.

## 12. Phụ lục

Phần này sẽ được bổ sung trong quá trình triển khai, bao gồm bảng số liệu baseline chi tiết, file `.clinerules` mẫu, prompt library hiện tại, template báo cáo CVE, danh sách các tình huống đáng chú ý đã log, và biên bản các buổi retrospective.