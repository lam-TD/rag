# Proposal mua máy phục vụ nghiên cứu AI Agent (LLM 7B/14B) – 4 users đồng thời (context không dài)

**Ngày:** 2026-01-09  
**Mục tiêu:** chạy/inference & thử nghiệm AI Agent với LLM cỡ **7B/14B**, phục vụ **~4 người dùng đồng thời**, ưu tiên thời gian phản hồi tốt, triển khai local (không phụ thuộc cloud).

---

## 1) Vì sao “không có GPU” thì model phản hồi chậm?

Các mô hình LLM chủ yếu là phép nhân ma trận rất lớn (GEMM) và thao tác tensor lặp đi lặp lại.  
- **GPU** có hàng nghìn nhân xử lý song song + băng thông bộ nhớ cao + thư viện tối ưu (CUDA/cuBLAS/FlashAttention…), nên chạy LLM nhanh hơn đáng kể.  
- **CPU** ít lõi hơn, băng thông RAM thấp hơn, nên cùng một workload sẽ **mất nhiều thời gian hơn** → thời gian “token đầu tiên” (TTFT) và tốc độ sinh token đều kém hơn.

> Kết luận: nếu mục tiêu là 7B/14B chạy mượt cho nhiều người đồng thời, **GPU rời là yếu tố quan trọng nhất**.

---

## 2) Hiện trạng: đang có Dell T400

Bạn đang có **NVIDIA T400 (thường 4GB VRAM)** – phù hợp CAD/đồ hoạ nhẹ, **không phù hợp** để chạy LLM 7B/14B “mượt” (VRAM thấp).  
Nguồn tham khảo thông số T400: NVIDIA/PNY datasheet.  

---

## 3) Assumptions thiết kế (theo yêu cầu của bạn)

- LLM mục tiêu: **7B/14B** (ưu tiên quantized 4-bit/8-bit), không yêu cầu context dài.  
- Đồng thời: **~4 users** (agent workflow có thể burst).  
- Ưu tiên: ổn định, dễ nâng cấp, linh kiện phổ biến ở VN.  
- Không bao gồm: màn hình, chuột phím, license OS.

---

## 4) Đề xuất cấu hình (3 phương án)

> Giá bên dưới là **giá tham khảo** (có thể thay đổi theo tồn kho/khuyến mãi).  
> Mình cố tình chọn **cùng “xương sống” CPU/RAM/SSD** để bạn dễ so sánh, khác nhau chủ yếu ở GPU + PSU.

### 4.1. BOM chung (áp dụng cả 3 phương án)

| Hạng mục | Đề xuất | Lý do |
|---|---|---|
| CPU | AMD Ryzen 9 7900 | 12C/24T cân tốt agent tooling + dịch vụ phụ trợ |
| Main | GIGABYTE B650 AORUS ELITE AX (DDR5) | AM5, ổn định, nhiều M.2, dễ nâng cấp |
| RAM | 64GB DDR5 6000 (2×32GB) | đủ cho 7B/14B + nhiều tiến trình |
| SSD | WD Black SN850X 2TB NVMe Gen4 | tốc độ cao, đủ chỗ cho model/artefacts |
| Tản CPU | DeepCool AK620 | hiệu năng/giá tốt |
| Case | Lian Li Lancool 216 | airflow tốt, dễ lắp GPU lớn |

---

### 4.2. Phương án A – “Value / bước đầu nghiên cứu” (RTX 4070 Ti SUPER 16GB)

**Phù hợp:** 7B/14B (quantized) + prototype agent; tối ưu chi phí, nhưng VRAM 16GB sẽ “chạm trần” nhanh hơn khi workload tăng.

| Hạng mục | Giá tham khảo (VND) | Nguồn |
|---|---:|---|
| CPU Ryzen 9 7900 | 10.490.000 | GearVN |
| Main B650 AORUS ELITE AX | 7.490.000 | GearVN |
| RAM 64GB DDR5 6000 (2×32GB) | 9.490.000 | Phong Vũ |
| SSD SN850X 2TB | 4.990.000 | GearVN |
| Tản nhiệt AK620 | 1.890.000 | GearVN |
| Case Lancool 216 | 2.039.000 | HugoTech |
| PSU MSI MAG A850GL PCIE5 850W | 2.790.000 | Phong Vũ |
| GPU RTX 4070 Ti SUPER 16GB (MSI Gaming X Slim) | 26.990.000 | GearVN |
| **Tổng** | **66.169.000** |  |

**Ghi chú kỹ thuật:** GPU này có thông tin tiêu thụ điện & PSU khuyến nghị trên trang sản phẩm.  

---

### 4.3. Phương án B – “Cân bằng” (RTX 4080 SUPER 16GB)

**Phù hợp:** hiệu năng cao hơn 4070 Ti SUPER, vẫn 16GB VRAM (tương tự giới hạn VRAM), hợp khi bạn ưu tiên tốc độ hơn chi phí.

| Hạng mục | Giá tham khảo (VND) | Nguồn |
|---|---:|---|
| (Các mục như phương án A, chỉ đổi GPU) |  |  |
| GPU RTX 4080 SUPER 16GB (MSI Gaming X Slim) | 33.990.000 | GearVN |
| **Tổng** | **73.169.000** |  |

---

### 4.4. Phương án C – “Khuyến nghị cho 14B + 4 users” (RTX 4090 24GB)

**Phù hợp:** bạn muốn chạy 14B thoải mái hơn (đặc biệt khi concurrent tăng), cần **VRAM 24GB** để giảm rủi ro OOM / giảm phải offload sang CPU.

| Hạng mục | Giá tham khảo (VND) | Nguồn |
|---|---:|---|
| CPU Ryzen 9 7900 | 10.490.000 | GearVN |
| Main B650 AORUS ELITE AX | 7.490.000 | GearVN |
| RAM 64GB DDR5 6000 (2×32GB) | 9.490.000 | Phong Vũ |
| SSD SN850X 2TB | 4.990.000 | GearVN |
| Tản nhiệt AK620 | 1.890.000 | GearVN |
| Case Lancool 216 | 2.039.000 | HugoTech |
| PSU Corsair RM1000e 1000W (ATX 3.x) | 4.390.000 | Phong Vũ |
| GPU RTX 4090 24GB (MSI Gaming X Trio) | 53.990.000 | GearVN |
| **Tổng** | **94.769.000** |  |

---

## 5) Khuyến nghị chọn phương án nào?

- Nếu **mục tiêu chính là 14B + 4 users đồng thời** và muốn “đỡ đau đầu” về VRAM: **chọn Phương án C (RTX 4090 24GB)**.  
- Nếu muốn **bắt đầu nhanh, tiết kiệm**, chấp nhận giới hạn VRAM và tối ưu bằng quantization: **Phương án A (4070 Ti SUPER 16GB)**.  
- Phương án B chỉ hợp khi bạn ưu tiên **tốc độ hơn A** nhưng vẫn chấp nhận **16GB VRAM**.

---

## 6) Gợi ý phần mềm triển khai (để tận dụng GPU tốt)

- Inference server: **vLLM** (nếu dùng model/format phù hợp) hoặc **llama.cpp** (GGUF) / **text-generation-inference**.
- Quantization gợi ý: **4-bit** (ưu tiên VRAM), hoặc **8-bit** (chất lượng/độ ổn định).
- Khi concurrent tăng: cân nhắc **batching**, giới hạn max_tokens, và queue theo session.

---

## 7) Rủi ro & lưu ý mua sắm

- Giá linh kiện thay đổi nhanh theo tồn kho/khuyến mãi.
- RTX 4090 kích thước lớn: cần kiểm tra **độ dài GPU** và clearance (Lancool 216 khá thoải mái).
- Nên ưu tiên PSU chuẩn **ATX 3.x + cáp 12VHPWR/12V-2x6** đúng chuẩn để an toàn.
- Nếu bạn muốn giữ case/PSU hiện tại (nếu có), cần kiểm tra: công suất PSU, số đầu PCIe, không gian trong case, airflow.

---

## 8) Nguồn tham khảo giá (links)

> Mục này để bạn bấm vào kiểm tra lại giá/tồn kho ngay khi chốt mua.

- CPU AMD Ryzen 9 7900 (GearVN): https://gearvn.com/products/amd-ryzen-9-7900  
- Mainboard GIGABYTE B650 AORUS ELITE AX (GearVN): https://gearvn.com/products/gigabyte-b650-aorus-elite-ax  
- GPU RTX 4070 Ti SUPER 16GB (GearVN): https://gearvn.com/products/card-man-hinh-msi-geforce-rtx-4070-ti-super-16g-gaming-x-slim  
- GPU RTX 4080 SUPER 16GB (GearVN): https://gearvn.com/products/card-man-hinh-msi-geforce-rtx-4080-super-16g-gaming-x-slim  
- GPU RTX 4090 (GearVN – MSI Gaming X Trio): https://gearvn.com/products/msi-geforce-rtx-4090-gaming-x-trio-24g  
- SSD WD Black SN850X 2TB (GearVN): https://gearvn.com/products/o-cung-ssd-wd-black-sn850x-2tb-m-2-pcie-nvme-gen-4-0  
- Tản nhiệt DeepCool AK620 (GearVN): https://gearvn.com/products/tan-nhiet-deepcool-ak620-ho-tro-socket-1700  
- Case Lian Li Lancool 216 (HugoTech): https://hugotech.vn/case-lian-li-lancool-216-black-g99lan216x00/  
- PSU MSI MAG A850GL PCIE5 (Phong Vũ): https://phongvu.vn/nguon-may-tinh-msi-mag-a850gl-pcie5-80-plus-gold-full-modular-306-7zp8a11-ce0--s230802065  
- PSU Corsair RM1000e 1000W (Phong Vũ): https://phongvu.vn/nguon-may-tinh-corsair-rm1000e-atx-3-1-cybenetics-gold-full-modul--s250309516  

---

## 9) Next step (nếu bạn muốn mình tối ưu thêm)

- Cho mình biết bạn muốn **ngân sách trần** (ví dụ 70m / 90m / 110m).  
- Bạn có muốn **2 GPU** để scale concurrent không (ví dụ 2×24GB), hay 1 GPU là đủ?  
- Bạn ưu tiên chạy model **GGUF (llama.cpp)** hay **HF (vLLM/TGI)**?