-----

## name: dieu-tra-lo-hong
description: Điều tra các lỗ hổng (CVE/advisory) có thể ảnh hưởng đến dự án Python/FastAPI này. Dùng khi cần kiểm kê phụ thuộc từ pyproject.toml/lockfile, đánh giá một CVE/advisory có thực sự ảnh hưởng codebase hay không, đề xuất cách khắc phục, hoặc viết báo cáo lỗ hổng. Kích hoạt khi người dùng dán mã CVE/advisory, hỏi “lỗ hổng này có ảnh hưởng dự án không”, hoặc yêu cầu rà soát/triage/báo cáo bảo mật phụ thuộc.

# Điều tra lỗ hổng (Python / FastAPI)

Mục tiêu: với mỗi lỗ hổng người dùng cung cấp, xác định nó có THỰC SỰ
ảnh hưởng dự án này không, đề xuất khắc phục, và viết báo cáo. Ưu tiên
độ chính xác và bằng chứng — không phỏng đoán, không quét tự động.

## Phạm vi (CHỈ làm 4 việc này)

Skill này KHÔNG quét tự động và KHÔNG tự chấm thang ưu tiên. Đầu vào lỗ
hổng do người dùng cung cấp. Chỉ thực hiện: Kiểm kê → Triage → Khắc phục
→ Báo cáo.

## Ranh giới tuyệt đối (KHÔNG được làm)

- KHÔNG chạy scanner hay `pip`, KHÔNG soi môi trường đã cài đặt.
- KHÔNG sửa `pyproject.toml`, lockfile hay mã nguồn. Chỉ đọc và đề xuất.
- KHÔNG tự bịa cấu trúc báo cáo khác với template.
- KHÔNG kết luận khi thiếu dữ liệu — phải hỏi lại người dùng.

## Điều kiện tiên quyết

Bước Triage cần tra web theo mã CVE (Cline websearch — yêu cầu Cline
provider có credit). Nếu KHÔNG tra web được: DỪNG bước đó và yêu cầu
người dùng dán phần mô tả advisory (hàm/feature dính lỗ, khoảng phiên
bản bị ảnh hưởng). Tuyệt đối không tự suy đoán chi tiết advisory.

## Quy trình

### 1. Kiểm kê phụ thuộc

- Đọc TĨNH `pyproject.toml` và lockfile có sẵn (poetry.lock /
  Pipfile.lock / uv.lock). Tự nhận loại lockfile và parse tương ứng.
- Lấy phiên bản từ lockfile (đây là phiên bản resolved thực tế).
- Dùng `pyproject.toml` để phân biệt: trực tiếp vs gián tiếp
  (transitive), runtime vs dev/test.
- Lưu ý các thành phần FastAPI hay dính lỗ: starlette, pydantic,
  uvicorn/gunicorn, python-multipart, jinja2, python-jose/pyjwt,
  sqlalchemy, httpx.

### 2. Triage theo ngữ cảnh

Với MỖI lỗ hổng người dùng dán vào:

1. Tra web theo mã CVE để lấy: hàm/feature dính lỗ, khoảng phiên bản
   bị ảnh hưởng, mã GHSA/OSV liên quan. (Không tra được → xem mục
   “Điều kiện tiên quyết”.)
1. Đối chiếu phiên bản resolved (bước 1) với khoảng bị ảnh hưởng.
1. Kiểm tra reachability bằng cách đọc code + grep trong repo:
- Package/hàm đó có được import không?
- Có nằm trên đường xử lý request (route FastAPI) không?
- Dữ liệu không tin cậy từ request có chạm tới nó không?
- Trước hay sau xác thực? Dịch vụ này có lộ ra Internet không?
1. Kết luận mỗi lỗ hổng vào MỘT trong ba nhãn, kèm bằng chứng:
- **Confirmed** — đúng phiên bản + reachable. Cần xử lý.
- **Low** — đúng phiên bản nhưng khó/không reachable, hoặc chỉ
  dev/test.
- **Not-applicable** — không ảnh hưởng. PHẢI nêu lý do có bằng
  chứng (sai khoảng phiên bản / không import / không reachable /
  có biện pháp bù đắp). Không chấp nhận lý do cảm tính.

### 3. Đề xuất khắc phục

Cho mỗi mục Confirmed:

- Phiên bản vá tối thiểu (lấy từ advisory đã tra ở bước Triage).
- Lệnh nâng cấp gợi ý (chỉ ghi ra, KHÔNG thực thi, KHÔNG sửa file).
- Cảnh báo rủi ro breaking change khi nâng major — đặc biệt
  Pydantic v1→v2, các bump lớn của FastAPI/Starlette — kèm gợi ý
  cần test gì trước khi merge.
- Nếu chưa có bản vá: nêu biện pháp giảm thiểu cụ thể (giới hạn
  input, tắt feature, chặn ở gateway/WAF, cô lập mạng).

### 4. Viết báo cáo

- Đọc template tại `templates/` trong thư mục skill (định dạng .md).
- Điền THEO ĐÚNG cấu trúc template, không thêm/bớt mục.
- Mỗi lỗ hổng một dòng ở bảng tổng hợp; chi tiết + bằng chứng ở
  phần riêng từng mục.
- Ghi báo cáo ra: `reports/vuln-report-<YYYY-MM-DD>.md` (đổi đường
  dẫn nếu người dùng yêu cầu khác).

## Khi không chắc

Nếu thiếu thông tin để kết luận (không tra được advisory, không xác
định được phiên bản, không rõ reachability) → DỪNG và hỏi người dùng,
không đưa kết luận tạm thời như thể đã xác nhận.