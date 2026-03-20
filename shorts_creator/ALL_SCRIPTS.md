# 📜 جميع السكربتات المتاحة

## 🎯 السكربتات الرئيسية

### **1. image_processor.py** 📸
```bash
python3 image_processor.py
```
**الوظيفة:** معالجة الصور وتحضيرها للذكاء الاصطناعي
**المدخلات:** صور في `input_images/`
**المخرجات:** صور محسنة في `enhanced_images/`
**المميزات:**
- تحسين الجودة والألوان
- تغيير الحجم للعمودي (1080x1920)
- اقتصاص ذكي مع الحفاظ على المحتوى

### **2. video_generator.py** 🤖
```bash
python3 video_generator.py
```
**الوظيفة:** تحويل الصور إلى فيديوهات باستخدام الذكاء الاصطناعي
**الخيارات:**
- `mock`: تجريبي بدون API (للتجربة)
- `runwayml`: استخدام RunwayML API (جودة عالية)
- `pika`: استخدام Pika Labs API (سهل الاستخدام)

### **3. video_assembler.py** 🎬
```bash
python3 video_assembler.py
```
**الوظيفة:** تجميع الفيديوهات في شورت نهائي
**المميزات:**
- إضافة عناوين وتأثيرات
- دمج مع موسيقى خلفية
- تحسين التوقيتات للمنصات

## 🚀 سكربتات الأتمتة

### **4. run_pipeline.sh** ⚡
```bash
./run_pipeline.sh
```
**الوظيفة:** تشغيل البايبلاين الكامل تلقائياً
**الخيارات:**
- 1: جميع الخطوات
- 2: معالجة الصور فقط
- 3: توليد الفيديو فقط
- 4: التجميع فقط

### **5. SIMPLE_EXAMPLE.sh** 🎯
```bash
./SIMPLE_EXAMPLE.sh
```
**الوظيفة:** دليل تفاعلي للمبتدئين
**المميزات:**
- إرشادات خطوة بخطوة
- تحقق من الملفات
- نصائح للخطوات التالية

## 🔧 سكربتات المساعدة

### **6. test_pipeline.py** 🧪
```bash
python3 test_pipeline.py
```
**الوظيفة:** اختبار جميع المكونات
**المخرجات:** تقرير مفصل عن حالة النظام

### **7. config.py** ⚙️
```python
from config import get_config_summary
```
**الوظيفة:** إدارة الإعدادات المركزية
**المحتوى:** جميع المتغيرات والمجلدات

## 📁 هيكل المجلدات

```
shorts_creator/
├── input_images/     ← ضع صورك هنا (يدوي)
├── enhanced_images/  ← الصور المحسنة (تلقائي)
├── generated_videos/ ← الفيديوهات المولدة (تلقائي)
├── final_videos/     ← الشورتات النهائية (تلقائي)
├── audio/            ← موسيقى خلفية (اختياري، يدوي)
├── *.py              ← السكربتات الرئيسية
├── *.sh              ← سكربتات الأتمتة
├── *.md              ← التوثيق
└── .env              ← الإعدادات (تعديل يدوي)
```

## 🎮 أمثلة استخدام

### **الطريقة السريعة:**
```bash
# 1. أضف صورك
cp ~/Pictures/vacation*.jpg input_images/

# 2. شغل البايبلاين
./run_pipeline.sh

# 3. اختر الخيار 1 (الكامل)
```

### **الطريقة التفصيلية:**
```bash
# 1. معالجة الصور
python3 image_processor.py

# 2. توليد الفيديو (مع RunwayML)
echo "runwayml" | python3 video_generator.py

# 3. التجميع النهائي
echo "1" | python3 video_assembler.py
```

### **للتجربة فقط:**
```bash
# 1. اختبار النظام
python3 test_pipeline.py

# 2. مثال بسيط
./SIMPLE_EXAMPLE.sh
```

## ⚡ نصائح سريعة

### **لبدء سريع:**
1. `./SIMPLE_EXAMPLE.sh` ← ابدأ هنا
2. أضف 3 صور إلى `input_images/`
3. اتبع التعليمات

### **للإنتاج الحقيقي:**
1. احصل على API key من RunwayML
2. أضفه إلى `.env`
3. `./run_pipeline.sh` ← اختار الخيار 1

### **للتحكم الكامل:**
1. `python3 image_processor.py`
2. `python3 video_generator.py` ← اختار `runwayml`
3. `python3 video_assembler.py` ← اختار `1`

## 🔍 استكشاف الأخطاء

### **تحقق من التثبيت:**
```bash
python3 test_pipeline.py
```

### **تحقق من الملفات:**
```bash
ls -la input_images/      # الصور الأصلية
ls -la enhanced_images/   # الصور المحسنة
ls -la generated_videos/  # الفيديوهات المولدة
ls -la final_videos/      # النتائج النهائية
```

### **تحقق من الإعدادات:**
```bash
cat .env 2>/dev/null || echo "استخدم .env.example كنموذج"
```

## 📞 الدعم

### **إذا واجهتك مشكلة:**
1. راجع `README.md` للتعليمات العامة
2. راجع `QUICK_START.md` للبدء السريع
3. جرب `test_pipeline.py` لفحص النظام
4. استخدم `SIMPLE_EXAMPLE.sh` للمساعدة التفاعلية

---

**🎬 كل السكربتات جاهزة للاستخدام!**  
اختر ما يناسب احتياجاتك وابدأ في إنشاء محتوى مذهل! ✨