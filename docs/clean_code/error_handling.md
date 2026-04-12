# Error Handling

## 1. Ưu tiên sử dụng Exception thay vì trả về mã lỗi

Thay vì trả về mã lỗi, hãy sử dụng Exception để xử lý lỗi. Điều này giúp mã của bạn trở nên rõ ràng hơn và dễ dàng bảo trì hơn bởi vì nó tách biệt logic xử lý lỗi khỏi logic chính của chương trình.

Bad

```python
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b
```

Good

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
```

Ví dụ PHP phức tạp trong thực tế

```php
function readFile($filename) {
    if (!file_exists($filename)) {
        throw new Exception("File not found: " . $filename);
    }

    $file = fopen($filename, "r");

    if (!$file) {
        throw new Exception("Unable to open file: " . $filename);
    }

    
    fclose($file);
}
```

## 2. Viết câu lệnh try-catch-finally trước tiên

Việc viết cấu trúc try-catch-finally trước khi viết logic giúp bạn xác định được phạm vi và trạng thái nhất quán của chương trình bất kể điều gì xảy ra trong khối try. Điều này giúp duy trì tính ổn định của hệ thống ngay từ khi bắt đầu thiết kế hàm.

1. Bắt đầu viết unit test cho hàm `retrieveSection` để xác định hành vi mong muốn khi có lỗi xảy ra.

    ```php
    public function testRetrieveSectionShouldThrowOnInvalidFileName() 
    {
        $this->expectException(StorageException::class);
        $this->sectionStore->retrieveSection("invalid-file");
    }
    ```

2. Tạo khung hàm (Stub)

    ```php
    public function retrieveSection(string $sectionName): array 
    {
        // Trả về mảng rỗng tạm thời cho đến khi có triển khai thực tế
        return [];
    }
    ```

3. Triển khai logic cơ bản để vượt qua bài Test

    ```php
    public function retrieveSection(string $sectionName): array 
    {
        try {
            // Giả định có một lớp hoặc hàm mở file throw an exception
            $stream = new FileInputStream($sectionName);
        } catch (Exception $e) {
            throw new StorageException("retrieval error", 0, $e);
        }
        return [];
    }
    ```

4. Refactor mã để đảm bảo rằng tài nguyên được quản lý đúng cách, ví dụ như đóng stream sau khi sử dụng.

    ```php
    public function retrieveSection(string $sectionName): array 
    {
        try {
            // Logic thực thi trong try có thể coi như một giao dịch (transaction)
            $stream = new FileInputStream($sectionName);
            $stream->close();
        } catch (FileNotFoundException $e) {
            // Bắt chính xác loại ngoại lệ và bọc lại bằng exception của ứng dụng
            throw new StorageException("retrieval error", 0, $e);
        }
        return [];
    }
    ```

Khái niệm TDD (Test-Driven Development) là một phương pháp phát triển phần mềm trong đó bạn viết các bài kiểm tra tự động trước khi viết mã thực tế.

Trong TDD, quy trình phát triển thường tuân theo ba bước chính:

1. **Viết bài kiểm tra thất bại (Red)**: Bạn bắt đầu bằng cách viết một bài kiểm tra tự động cho một tính năng hoặc chức năng mới mà bạn muốn triển khai. Vì bạn chưa viết mã thực tế, bài kiểm tra này sẽ thất bại khi chạy.
2. **Viết mã thực tế (Green)**: Sau khi có bài kiểm tra thất bại, bạn viết mã thực tế để làm cho bài kiểm tra đó thành công. Mục tiêu là viết đủ mã để vượt qua bài kiểm tra mà không cần phải lo lắng về việc tối ưu hóa hoặc thiết kế hoàn hảo.
3. **Tối ưu hóa mã (Refactor)**: Khi bài kiểm tra đã thành công, bạn có thể tối ưu hóa mã của mình mà không lo lắng về việc phá vỡ chức năng, vì bạn đã có bài kiểm tra tự động đảm bảo rằng mọi thứ vẫn hoạt động đúng sau khi bạn thực hiện các thay đổi.

## 3. Ưu tiên sử dụng Exception chưa kiểm duyệt (Unchecked Exceptions)

## 4. Cung cấp ngữ cảnh với Exception

Khi ném một Exception, hãy cung cấp càng nhiều ngữ cảnh càng tốt để giúp người phát triển hiểu rõ nguyên nhân của lỗi.
Điều này có thể bao gồm:

- Thông tin về trạng thái của chương trình
- Giá trị của các biến liên quan
- Hoặc bất kỳ thông tin nào khác có thể hữu ích để chẩn đoán vấn đề.

> Note: Tránh cung cấp quá nhiều thông tin nhạy cảm trong Exception, đặc biệt là trong môi trường sản xuất, để tránh rủi ro bảo mật.

Bad

```python
def process_data(data):
    if not isinstance(data, list):
        raise ValueError("Invalid data type")
    # Xử lý dữ liệu
```

Good

```python
def process_data(data):
    if not isinstance(data, list):
        raise ValueError(f"Invalid data type: expected list but got {type(data).__name__}")
    # Xử lý dữ liệu
```

## 5. Định nghĩa các lớp Ngoại lệ theo nhu cầu của người gọi

Thay vì thiết kế ngoại lệ theo nguồn gốc kỹ thuật của lỗi, hãy thiết kế chúng theo cách phía gọi cần xử lý.

Hãy bao bọc (wrap) exception của thư viện hoặc framework bên thứ ba thành các exception mang ý nghĩa của ứng dụng.
Cách này mang lại nhiều lợi ích:

- Giảm phụ thuộc vào thư viện bên ngoài
- Làm cho API nội bộ dễ đọc hơn
- Dễ dàng thay đổi: Khi đổi thư viện, chỉ sửa ở lớp bao bọc, không phải sửa toàn hệ thống.

Bad

```php
class ChatApiGateway {
    public function __construct(private GuzzleHttp $httpClient) {}

    public function getChatById(string $chatId): array
    {
        try {
            $response = $this->httpClient->request('GET', "/chats/{$chatId}");
            $data = json_decode((string) $response->getBody(), true);

            if (!is_array($data)) {
                throw new ChatServiceUnavailableException('Invalid response from Chat service.');
            }

            return $data;
        } catch (\GuzzleHttp\Exception\ConnectException $e) {
            // xử lý lỗi kết nối
        } catch (\GuzzleHttp\Exception\ClientException $e) {
            // xử lý lỗi 4xx
        } catch (\GuzzleHttp\Exception\ServerException $e) {
            // xử lý lỗi 5xx
        } catch (GuzzleException $e) {
            // Bắt lỗi của Guzzle
            throw $e;
        }
    }
}
```

Cách làm này không tốt vì nó gắn chặt vào thư viện Guzzle, nếu sau này muốn đổi sang thư viện khác sẽ phải sửa toàn bộ mã xử lý lỗi.

Good

```php
<?php

interface HttpClientInterface {
    public function request(string $method, string $url, array $options = []): HttpResponse;
}

class HttpClientException extends RuntimeException {}
class NetworkException extends HttpClientException {}
class TimeoutException extends HttpClientException {}
class InvalidResponseException extends HttpClientException {}

class HttpRequestException extends HttpClientException {}

final class GuzzleHttpClient implements HttpClientInterface {
    public function request(string $method, string $url, array $options = []): HttpResponse
    {
        try {
            // Logic thực hiện HTTP request
        } catch (\GuzzleHttp\Exception\ConnectException $e) {
            // xử lý lỗi kết nối
            throw new NetworkException('Network error occurred.', previous: $e);
        } catch (\GuzzleHttp\Exception\ClientException $e) {
            // xử lý lỗi 4xx
            throw new HttpRequestException('Client error occurred.', previous: $e);
        } catch (\GuzzleHttp\Exception\ServerException $e) {
            // xử lý lỗi 5xx
            throw new HttpRequestException('Server error occurred.', previous: $e);
        } catch (GuzzleException $e) {
            // Bắt lỗi của Guzzle
            throw new HttpClientException('HTTP request failed.', previous: $e);
        }
    }
}

```

```php
<?php

namespace App\Exceptions;

use RuntimeException;

class ChatServiceException extends RuntimeException
{
}

class ChatNotFoundException extends ChatServiceException
{
}

class ChatServiceUnavailableException extends ChatServiceException
{
}
```

Bước 2: Bọc thư viện bên thứ ba bằng một lớp bao bọc (Wrapper)

```php
<?php

class ChatApiGateway
{
    public function __construct(private HttpClientInterface $httpClient) {}

    public function getChatById(string $chatId): array
    {
        try {
            $response = $this->httpClient->request('GET', "/chats/{$chatId}");
            $data = json_decode((string) $response->getBody(), true);

            if (!is_array($data)) {
                throw new ChatServiceUnavailableException('Invalid response from Chat service.');
            }

            return $data;
        } catch (ClientException $e) {
            $statusCode = $e->getResponse()?->getStatusCode();

            if ($statusCode === 404) {
                throw new ChatrNotFoundException(
                    "Chat {$chatId} not found.",
                    previous: $e
                );
            }

            throw new ChatServiceUnavailableException(
                'Chat service returned an unexpected client error.',
                previous: $e
            );
        } catch (ConnectException $e) {
            throw new ChatServiceUnavailableException(
                'Cannot connect to Chat service.',
                previous: $e
            );
        } catch (GuzzleException $e) {
            throw new ChatServiceUnavailableException(
                'Chat service request failed.',
                previous: $e
            );
        }
    }
}


## 6. Xác định luồng xử lý bình thường (Normal Flow)

## 7. Không trả về Null và không truyền Null