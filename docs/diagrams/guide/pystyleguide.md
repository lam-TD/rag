
### 2.2 Imports

Chỉ dùng câu lệnh `import` để import **package** và **module**, không import trực tiếp từng **type**, **class**, hay **function**.

#### 2.2.1 Định nghĩa

Cơ chế tái sử dụng để chia sẻ code từ module này sang module khác.

#### 2.2.2 Ưu điểm

Quy ước quản lý namespace đơn giản. Nguồn gốc của mỗi định danh (identifier) được thể hiện nhất quán;  
`x.Obj` cho biết đối tượng `Obj` được định nghĩa trong module `x`.

#### 2.2.3 Nhược điểm

Tên module vẫn có thể bị trùng nhau. Một số tên module dài và bất tiện khi sử dụng.

#### 2.2.4 Quyết định

- Dùng `import x` để import package và module.
- Dùng `from x import y` khi `x` là package prefix và `y` là tên module (không kèm prefix).
- Dùng `from x import y as z` trong các trường hợp sau:
  - Có hai module cùng tên `y` cần import.
  - `y` trùng với tên top-level được định nghĩa trong module hiện tại.
  - `y` trùng với tên tham số phổ biến thuộc public API (ví dụ: `features`).
  - `y` quá dài hoặc bất tiện.
  - `y` quá chung chung trong ngữ cảnh code của bạn (ví dụ: `from storage.file_system import options as fs_options`).
- Chỉ dùng `import y as z` khi `z` là viết tắt chuẩn (ví dụ: `import numpy as np`).

Ví dụ module `sound.effects.echo` có thể import như sau:

```python
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

Không dùng relative import. Dù module nằm trong cùng package, hãy dùng full package name.
Điều này giúp tránh việc vô tình import cùng một package hai lần.

##### 2.2.4.1 Ngoại lệ (Exemptions)

Các ngoại lệ cho quy tắc này:

- Các **symbol** từ những module sau được phép import trực tiếp để phục vụ **phân tích tĩnh (static analysis)** và **kiểm tra kiểu (type checking)**:
  - Module `typing`
  - Module `collections.abc`
  - Module `typing_extensions`

- Các **redirects** từ module `six.moves`.


### 2.3 Packages

Import mỗi module bằng **đường dẫn đầy đủ (full pathname)** của module đó.

#### 2.3.1 Ưu điểm

Tránh xung đột tên module hoặc import sai do **module search path** không đúng như tác giả mong đợi. Đồng thời giúp việc tìm module dễ hơn.

#### 2.3.2 Nhược điểm

Làm việc deploy khó hơn vì bạn phải tái tạo đúng **cấu trúc phân cấp package**. Tuy nhiên, với cơ chế deploy hiện đại thì đây thường không còn là vấn đề lớn.

#### 2.3.3 Quyết định

Tất cả code mới nên import mỗi module bằng **tên package đầy đủ**.

Import nên như sau:

```python
Yes:
  # Tham chiếu absl.flags bằng tên đầy đủ (dài nhưng rõ ràng).
  import absl.flags
  from doctor.who import jodie

  _FOO = absl.flags.DEFINE_string(...)
```

```python
Yes:
  # Tham chiếu flags bằng tên module ngắn (phổ biến).
  from absl import flags
  from doctor.who import jodie

  _FOO = flags.DEFINE_string(...)
```
(giả sử file này nằm trong doctor/who/ và jodie.py cũng nằm ở đó)

```python
No:
  # Không rõ tác giả muốn import module nào và sẽ import cái gì.
  # Hành vi import thực tế phụ thuộc vào các yếu tố bên ngoài điều khiển sys.path.
  # Tác giả muốn import "jodie" nào trong các khả năng?
  import jodie
```
Không nên giả định rằng thư mục chứa main binary luôn có trong sys.path (dù một số môi trường có thể “vô tình” làm vậy). Vì thế, code nên hiểu rằng import jodie đang trỏ tới một package jodie thuộc bên thứ ba hoặc top-level, không phải file local jodie.py.

2.4 Exceptions

Exception được phép dùng nhưng phải cẩn thận.

2.4.1 Định nghĩa

Exception là một cách để “thoát” khỏi luồng điều khiển bình thường nhằm xử lý lỗi hoặc các tình huống bất thường.

2.4.2 Ưu điểm

Luồng code chạy bình thường không bị “rối” bởi logic xử lý lỗi. Ngoài ra, nó cho phép bỏ qua nhiều stack frame khi xảy ra điều kiện đặc biệt (ví dụ: thoát khỏi N hàm lồng nhau trong một bước thay vì phải truyền error code qua từng lớp).

2.4.3 Nhược điểm

Có thể làm luồng điều khiển khó hiểu. Dễ bỏ sót các trường hợp lỗi khi gọi thư viện.

2.4.4 Quyết định

Exception phải tuân theo các điều kiện sau:

Ưu tiên dùng exception built-in khi hợp lý. Ví dụ: raise ValueError để chỉ ra lỗi lập trình như vi phạm điều kiện tiên quyết (precondition), chẳng hạn khi validate tham số hàm.

Không dùng assert để thay thế điều kiện/validate precondition. assert không được phép trở thành phần “sống còn” của logic ứng dụng. Một cách kiểm tra nhanh: nếu bỏ assert mà code vẫn chạy đúng logic thì mới ổn. Các biểu thức assert không được đảm bảo sẽ luôn được evaluate. Với test dùng pytest, assert là hợp lệ và thường dùng để verify kỳ vọng. Ví dụ:

```python
Yes:
  def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    if minimum < 1024:
      # Việc raise ValueError này không liệt kê trong "Raises:" vì không phù hợp
      # để “cam kết” hành vi cụ thể khi API bị dùng sai.
      raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
    port = self._find_next_open_port(minimum)
    if port is None:
      raise ConnectionError(
          f'Could not connect to service on port {minimum} or higher.')
    # Code không phụ thuộc vào kết quả của assert này.
    assert port >= minimum, (
        f'Unexpected port {port} when minimum was {minimum}.')
    return port
```
```python
No:
  def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.
    """
    assert minimum >= 1024, 'Minimum port must be at least 1024.'
    # Đoạn code phía dưới phụ thuộc vào assert phía trên.
    port = self._find_next_open_port(minimum)
    assert port is not None
    # Việc type checking của return phụ thuộc vào assert.
    return port

```
Thư viện/package có thể định nghĩa exception riêng. Khi làm vậy:

phải kế thừa từ một exception có sẵn,

tên exception nên kết thúc bằng Error,

tránh lặp lại không cần thiết (ví dụ: foo.FooError).

Không bao giờ dùng except: kiểu bắt tất cả, hoặc bắt Exception/StandardError, trừ khi bạn:

raise lại exception, hoặc

tạo “điểm cách ly” (isolation point) nơi exception không được propagate mà được ghi nhận và suppressed, ví dụ: bảo vệ thread không bị crash bằng cách bao outermost block.

Python “rất dễ dãi” trong việc bắt lỗi: except: sẽ bắt cả mọi thứ như tên bị gõ sai, sys.exit(), Ctrl+C interrupt, unittest failures… và nhiều thứ khác mà bạn không hề muốn bắt.

Giảm tối đa code trong try/except. try càng lớn thì càng dễ có dòng code ném exception mà bạn không ngờ tới; khi đó try/except có thể che mất lỗi thật.

Dùng finally để chạy đoạn code dù có exception hay không, thường để cleanup (ví dụ: đóng file).