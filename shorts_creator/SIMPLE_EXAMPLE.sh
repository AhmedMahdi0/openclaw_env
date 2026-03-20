#!/bin/bash
# مثال بسيط لإنشاء شورت باستخدام الذكاء الاصطناعي

echo "🎬 مثال عملي لإنشاء شورت بالذكاء الاصطناعي"
echo "=========================================="

# 1. أنشئ مجلد للصور إذا لم يكن موجوداً
mkdir -p input_images

echo ""
echo "📸 الخطوة 1: أضف صورك إلى مجلد input_images/"
echo "   (يمكنك نسخ 3 صور من هاتفك أو جهازك)"
echo ""
echo "   مثلاً:"
echo "   - صورة طفولة"
echo "   - صورة من رحلة"
echo "   - صورة حديثة"
echo ""
read -p "   اضغط Enter عندما تكون الصور جاهزة..."

# 2. معالجة الصور
echo ""
echo "🔄 الخطوة 2: معالجة الصور..."
python3 image_processor.py

# 3. توليد فيديوهات تجريبية
echo ""
echo "🤖 الخطوة 3: توليد فيديوهات تجريبية..."
echo "1" | python3 video_generator.py

# 4. التحقق من النتائج
echo ""
echo "📁 الخطوة 4: التحقق من الملفات المولدة..."
echo ""
echo "الملفات المولدة:"
echo "----------------"
find enhanced_images -name "*.jpg" 2>/dev/null | head -5
find generated_videos -name "*.mp4" 2>/dev/null | head -5
find generated_videos -name "*.txt" 2>/dev/null | head -5

# 5. نصائح للخطوة التالية
echo ""
echo "🚀 الخطوة التالية:"
echo "-----------------"
echo "1. للحصول على نتائج حقيقية:"
echo "   - سجل في RunwayML أو Pika Labs"
echo "   - احصل على API Key"
echo "   - أضفه إلى ملف .env"
echo ""
echo "2. ثم أعد التشغيل:"
echo "   python3 video_generator.py"
echo "   (اختر runwayml أو pika)"
echo ""
echo "3. أخيراً:"
echo "   python3 video_assembler.py"
echo ""
echo "🎉 وستحصل على شورت جاهز للنشر!"

# 6. عرض هيكل المشروع
echo ""
echo "📂 هيكل المشروع:"
echo "---------------"
ls -la input_images/ 2>/dev/null | grep -E "\.(jpg|jpeg|png)$" | head -5
if [ $? -ne 0 ]; then
    echo "   (لا توجد صور بعد)"
fi

echo ""
echo "✅ المهمة انتهت!"
echo "   يمكنك الآن استكشاف الملفات المولدة."