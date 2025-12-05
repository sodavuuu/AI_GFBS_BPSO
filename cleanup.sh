#!/bin/bash
# Script dọn dẹp file trùng lặp trong project

echo "🧹 Bắt đầu dọn dẹp project..."

# 1. Xóa thư mục notebooks (trùng với experiment/)
echo ""
echo "📁 Xóa thư mục notebooks/ (trùng với experiment/)..."
if [ -d "notebooks" ]; then
    rm -rf notebooks/
    echo "   ✅ Đã xóa notebooks/"
else
    echo "   ℹ️  Thư mục notebooks/ không tồn tại"
fi

# 2. Xóa tất cả .ipynb_checkpoints
echo ""
echo "📁 Xóa tất cả .ipynb_checkpoints/..."
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null
echo "   ✅ Đã xóa .ipynb_checkpoints/"

# 3. Xóa tất cả __pycache__
echo ""
echo "📁 Xóa tất cả __pycache__/..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "   ✅ Đã xóa __pycache__/"

# 4. Xóa các file .pyc
echo ""
echo "📄 Xóa các file .pyc..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "   ✅ Đã xóa .pyc files"

# 5. Tổng kết
echo ""
echo "✨ Hoàn thành dọn dẹp!"
echo ""
echo "📊 Cấu trúc sau khi dọn dẹp:"
tree -L 2 -I '__pycache__|.ipynb_checkpoints|.git' . 2>/dev/null || ls -R

echo ""
echo "⚠️  LƯU Ý:"
echo "   - Đã xóa thư mục notebooks/ (giữ experiment/)"
echo "   - Chỉ còn 1 bộ notebooks trong experiment/"
echo "   - Đã xóa tất cả backup và cache files"
