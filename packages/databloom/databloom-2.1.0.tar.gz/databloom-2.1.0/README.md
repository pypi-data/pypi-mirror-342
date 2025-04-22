# DataBloom SDK Client

A Python SDK client for data integration with PostgreSQL, MySQL, Nessie, and S3.

## Quick Start

```bash
# Setup environment
conda create -n data_bloom python=3.11
conda activate data_bloom

# Install
pip install -e ".[dev]"
```

## Configuration

Create `.env` file with your credentials:

## Testing

```bash
# Run all tests
make test
```

## Development

```bash
make format          # Format code
make lint           # Run linter
make doc            # Build docs
```

## License

VNG License


# Update TODO list (tuần 2025-04-14)

Mục tiêu tạo use case thực tế phức tạp + yêu cầu performance
Cần đảm bảo secure + performance

# Giải quyết các vấn đề còn tồn đọng
- [ ] Implement với SQLAlchemy để tạo sample workflow trên Windmill (support use case phức tạp, data nhẹ)
- [ ] Cần authen đến dataset theo Backend (@chinhtt)
- [ ] Implement với SQLAlchemy để tạo sample workflow trên Windmill (Đã PoC)
- [ ] Performance chạy worker thao tác trên windmill low performance
- [ ] Performance chạy spark cluster cho các task cần high performance
- [ ] Dev tiếp phần SDK server ( support spark job submit qua cluster để chủ động được các thành phần trong worker)

## Hỗ trợ thêm các connector khác (cần @hainv4 support)
- [ ] Oracle  
- [ ] SAP 
- [ ] MS SQL Server

## Tạo bộ code block chứa các action dùng SDK tương tác hệ thống
- [ ] Ggsheet  
- [ ] Postgresql
- [ ] MySQL
- [ ] MongoDB
- [ ] S3 
- [ ] Dataset


