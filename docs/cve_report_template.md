# CVE Impact Assessment Report Template

> Mục tiêu: Chuẩn hoá cách team dev điều tra CVE hằng tuần để xác định: CVE có ảnh hưởng đến dự án không, mức độ ưu tiên xử lý, hành động cần thực hiện, người chịu trách nhiệm và bằng chứng xác minh.

---

## 1. Thông tin chung

| Field | Nội dung |
|---|---|
| Report ID | CVE-REPORT-YYYY-MM-DD-001 |
| Ngày báo cáo | YYYY-MM-DD |
| Người điều tra |  |
| Reviewer |  |
| Dự án / Service |  |
| Môi trường ảnh hưởng | Dev / Staging / Production / Internal Tool |
| Trạng thái báo cáo | Draft / In Review / Approved / Closed |
| Link ticket |  |

---

## 2. Executive Summary

### Kết luận nhanh

| Câu hỏi | Kết luận |
|---|---|
| CVE có liên quan đến dự án không? | Yes / No / Unknown |
| Dự án có đang dùng package/component bị ảnh hưởng không? | Yes / No / Unknown |
| Version hiện tại có nằm trong affected range không? | Yes / No / Unknown |
| Có bằng chứng bị khai thác thực tế không? | Yes / No / Unknown |
| Có expose ra internet không? | Yes / No / Unknown |
| Mức độ ưu tiên xử lý | Critical / High / Medium / Low |
| Quyết định | Patch / Mitigate / Monitor / Accept Risk / Not Applicable |

### Tóm tắt 3–5 dòng

```text
CVE này ảnh hưởng đến [component/package].
Dự án [có/không] sử dụng component này tại [service/module].
Version hiện tại là [x.y.z], [nằm/không nằm/chưa xác định] trong affected range.
Rủi ro chính là [RCE/data leak/auth bypass/DoS/...].
Khuyến nghị: [upgrade lên version ... / cấu hình mitigation / không cần action].
```

---

## 3. CVE Metadata

| Field | Nội dung |
|---|---|
| CVE ID | CVE-YYYY-NNNN |
| Tên / Mô tả ngắn |  |
| Nguồn tham khảo chính | NVD / Vendor Advisory / GitHub Security Advisory / CISA KEV / FIRST EPSS |
| Ngày công bố |  |
| Ngày cập nhật gần nhất |  |
| Vendor / Product |  |
| Component / Package |  |
| Affected versions |  |
| Fixed versions |  |
| CVSS score |  |
| CVSS vector |  |
| EPSS score / percentile |  |
| Có trong CISA KEV? | Yes / No |
| Exploit public? | Yes / No / Unknown |
| Exploit in the wild? | Yes / No / Unknown |

---

## 4. Mô tả lỗ hổng

### 4.1 Tóm tắt kỹ thuật

```text
Lỗ hổng xảy ra do [nguyên nhân kỹ thuật].
Kẻ tấn công có thể [hành động khai thác].
Điều kiện cần để khai thác là [authentication/network access/user interaction/configuration/...].
Tác động có thể là [confidentiality/integrity/availability].
```

### 4.2 Loại tác động

| CIA | Có ảnh hưởng? | Mô tả |
|---|---:|---|
| Confidentiality | Yes / No | Có thể rò rỉ dữ liệu gì? |
| Integrity | Yes / No | Có thể sửa/xoá/thao túng dữ liệu không? |
| Availability | Yes / No | Có thể gây gián đoạn dịch vụ không? |

---

## 5. Kiểm tra mức độ liên quan đến dự án

### 5.1 Component inventory

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Package/component có trong dependency manifest không? | Yes / No | composer.lock / package-lock.json / requirements.txt / Dockerfile |
| Component có trong container image không? | Yes / No | SBOM / image scan |
| Component có trong transitive dependency không? | Yes / No | dependency tree |
| Component có được load/runtime không? | Yes / No | config / import / service usage |
| Component nằm trong service nào? |  |  |
| Component có ở production không? | Yes / No | deploy manifest / environment |

### 5.2 Version check

| Service | Component | Current version | Affected range | Fixed version | Affected? |
|---|---|---:|---:|---:|---|
|  |  |  |  |  | Yes / No / Unknown |

### 5.3 Exposure check

| Câu hỏi | Kết quả | Ghi chú |
|---|---|---|
| Service có public internet không? | Yes / No |  |
| Cần authentication để chạm tới vulnerable path không? | Yes / No |  |
| Có WAF / API Gateway / rate limit không? | Yes / No |  |
| Có dùng feature/config bị ảnh hưởng không? | Yes / No |  |
| Attack vector là network/local/physical? |  |  |
| Có dữ liệu nhạy cảm liên quan không? | Yes / No |  |

---

## 6. Risk Assessment

### 6.1 Risk scoring nội bộ

| Tiêu chí | Điểm |
|---|---:|
| CVSS severity: Critical=4, High=3, Medium=2, Low=1 |  |
| Có trong CISA KEV: Yes=4, No=0 |  |
| Exploit public/in the wild: Yes=4, Unknown=2, No=0 |  |
| Component đang dùng ở production: Yes=3, No=0 |  |
| Public internet exposure: Yes=3, Internal=1, No=0 |  |
| Có dữ liệu nhạy cảm/PII/token/secrets: Yes=3, No=0 |  |
| Không có mitigation hiện tại: Yes=2, No=0 |  |
| Khó patch / downtime cao: Yes=1, No=0 |  |
| Tổng điểm |  |

### 6.2 Mức ưu tiên xử lý

| Tổng điểm | Priority | SLA đề xuất |
|---:|---|---|
| >= 15 | Critical | Fix/Mitigate trong 24–48h |
| 10–14 | High | Fix trong 3–7 ngày |
| 6–9 | Medium | Fix trong sprint hiện tại hoặc sprint kế tiếp |
| 1–5 | Low | Monitor / plan theo backlog |
| 0 | Not Applicable | Close với bằng chứng |

---

## 7. Quyết định xử lý

| Option | Khi nào dùng | Kết luận |
|---|---|---|
| Patch | Có fixed version và upgrade khả thi |  |
| Mitigate | Chưa patch được ngay, nhưng có workaround |  |
| Monitor | Chưa ảnh hưởng trực tiếp nhưng cần theo dõi |  |
| Accept Risk | Rủi ro thấp/chấp nhận được, có approval |  |
| Not Applicable | Không dùng component hoặc version không bị ảnh hưởng |  |

### Quyết định cuối cùng

```text
Decision: Patch / Mitigate / Monitor / Accept Risk / Not Applicable

Lý do:
- ...
- ...
- ...

Người approve:
- ...
```

---

## 8. Remediation Plan

| Action item | Owner | Deadline | Status | Evidence |
|---|---|---|---|---|
| Upgrade package/component lên version fixed |  |  | To do / Doing / Done | PR link |
| Chạy regression test |  |  |  | Test report |
| Rebuild container image |  |  |  | Image digest |
| Deploy staging |  |  |  | Deployment link |
| Deploy production |  |  |  | Release note |
| Verify scanner không còn detect |  |  |  | Scan result |

---

## 9. Verification Checklist

- [ ] Đã xác nhận version trước khi fix.
- [ ] Đã xác nhận affected range từ nguồn chính thức/vendor.
- [ ] Đã xác nhận fixed version.
- [ ] Đã kiểm tra direct dependency.
- [ ] Đã kiểm tra transitive dependency.
- [ ] Đã kiểm tra container/base image.
- [ ] Đã kiểm tra service có deploy production hay không.
- [ ] Đã kiểm tra exposure: public/internal/auth required.
- [ ] Đã đánh giá tác động CIA.
- [ ] Đã tạo PR/ticket remediation nếu cần.
- [ ] Đã chạy test liên quan.
- [ ] Đã scan lại sau khi fix.
- [ ] Đã cập nhật conclusion và evidence.

---

## 10. Evidence

### 10.1 Dependency evidence

```bash
# Ví dụ
composer show vendor/package
npm ls package-name
pipdeptree | grep package-name
docker sbom image-name
```

### 10.2 Scanner evidence

```text
Tool:
Scan date:
Finding:
Result:
```

### 10.3 Source references

| Source | Link / Reference | Ghi chú |
|---|---|---|
| NVD |  |  |
| Vendor Advisory |  |  |
| GitHub Security Advisory |  |  |
| CISA KEV |  |  |
| FIRST EPSS |  |  |
| Internal ticket / PR |  |  |

---

## 11. Final Status

| Field | Nội dung |
|---|---|
| Final status | Closed / Monitoring / Remediation in progress |
| Residual risk | None / Low / Medium / High |
| Risk acceptance required? | Yes / No |
| Approved by |  |
| Closed date |  |
| Lesson learned |  |

---

## 12. Example Conclusion

```text
Conclusion:
CVE-YYYY-NNNN does not currently affect our production environment.

Reason:
- The vulnerable package exists only in devDependencies.
- It is not included in the production container image.
- The vulnerable function is not used by our application.
- Production scan on YYYY-MM-DD did not detect the affected version.

Decision:
Not Applicable. No remediation required at this time.

Next step:
Continue monitoring vendor advisory and dependency scan results.
```
