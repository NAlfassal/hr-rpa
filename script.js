// تعيين الحد الأدنى لتاريخ النشاط (قبل اليوم الحالي)
const today = new Date();
const maxDate = today.toISOString().split('T')[0];
document.getElementById('activityDate').setAttribute('max', maxDate);

document.getElementById('knowledgeForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // إظهار رسالة التحميل
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    const formData = new FormData(this);

    try {
        const response = await fetch('http://localhost:5000/submit', {
            method: 'POST',
            body: formData,
        });

        document.getElementById('loading').style.display = 'none';

        if (response.ok) {
            const resultText = await response.text();

            // عرض رسالة النجاح من الخادم
            const successDiv = document.getElementById('successMessage');
            successDiv.innerHTML = `<h3>${resultText}</h3>`;
            successDiv.style.display = 'block';
            successDiv.scrollIntoView({ behavior: 'smooth' });

            // إعادة تعيين النموذج بعد 3 ثوانٍ
            setTimeout(function () {
                document.getElementById('knowledgeForm').reset();
                successDiv.style.display = 'none';
                window.scrollTo({ top: 0, behavior: 'smooth' });
                // إعادة تعيين قائمة الإدارات عند إعادة تعيين النموذج
                updateDepartments();
            }, 3000);

        } else {
            console.error('❌ فشل في حفظ الرد');
            alert('حدث خطأ أثناء إرسال النموذج. الرجاء المحاولة مجدداً.');
        }
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        console.error('⚠️ خطأ في الاتصال بالسيرفر:', error);
        alert('فشل في الاتصال بخادم حفظ البيانات.');
    }
});

// إضافة تأثيرات تفاعلية للحقول
const formControls = document.querySelectorAll('.form-control');
formControls.forEach(control => {
    control.addEventListener('focus', function () {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.3s ease';

        const existingError = this.parentElement.querySelector('.error-message');
        if (existingError) existingError.remove();

        this.style.borderColor = '#e0e0e0';
        this.style.boxShadow = 'none';
    });

    control.addEventListener('input', function () {
        if (this.hasAttribute('required')) {
            let isValid = false;

            if (this.type === 'select-one') {
                isValid = this.value !== '';
            } else if (this.type === 'number') {
                isValid = this.value !== '' && parseFloat(this.value) > 0;
            } else {
                isValid = this.value.trim() !== '';
            }

            if (isValid) {
                this.style.borderColor = '#4caf50';
                this.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.2)';
                const existingError = this.parentElement.querySelector('.error-message');
                if (existingError) existingError.remove();
            }
        }
    });

    control.addEventListener('blur', function () {
        this.parentElement.style.transform = 'scale(1)';

        if (this.hasAttribute('required')) {
            let isEmpty = false;

            if (this.type === 'select-one') {
                isEmpty = this.value === '';
            } else if (this.type === 'number') {
                isEmpty = this.value === '' || parseFloat(this.value) <= 0;
            } else {
                isEmpty = this.value.trim() === '';
            }

            if (isEmpty) {
                this.style.borderColor = '#f44336';
                this.style.boxShadow = '0 0 0 3px rgba(244, 67, 54, 0.2)';

                const existingError = this.parentElement.querySelector('.error-message');
                if (!existingError) {
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    errorMessage.style.cssText = `
                        color: #f44336;
                        font-size: 13px;
                        margin-top: 5px;
                        padding: 5px 10px;
                        background: rgba(244, 67, 54, 0.1);
                        border-radius: 5px;
                        border-right: 3px solid #f44336;
                    `;
                    errorMessage.textContent = 'هذا الحقل مطلوب ولا يمكن تركه فارغاً';
                    this.parentElement.appendChild(errorMessage);
                }
            }
        }
    });
});

// التحقق من صحة التاريخ
document.getElementById('activityDate').addEventListener('change', function () {
    const selectedDate = new Date(this.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate > today) {
        alert('يجب أن يكون تاريخ النشاط قبل اليوم الحالي أو في اليوم الحالي');
        this.value = '';
    }
});


const sectorsAndDepartments = {
    "قطاع الغذاء": [
        "مكتب القطاع",
        "الرصد وتقييم المخاطر",
        "المواصفات وتقييم المنتجات الغذائية",
        "التغذية",
        "منتجات التبغ",
        "الأمانة العامة للجنة الوطنية للتغذية",
        "اتصالات مخاطر ومنافع الغذاء"
    ],
    "قطاع الدواء": [
        "مكتب القطاع",
        "تقييم المنافع والمخاطر",
        "الشؤون التنظيمية",
        "تقييم جودة الأدوية",
        "التيقظ الدوائي",
        "المستحضرات البيطرية"
    ],
    "قطاع الأجهزة والمنتجات الطبية": [
        "مكتب القطاع",
        "تقييم الأجهزة الطبية",
        "الصحة الإشعاعية",
        "الرقابة والقياسات الحيوية",
        "الشؤون التنظيمية"
    ],
    "قطاع العمليات": [
        "مكتب القطاع",
        "الرقابة على المصانع",
        "توفر المنتجات",
        "التسجيل والتراخيص",
        "المطابقة و إنفاذ الأنظمة",
        "مركز الحلال",
        "الفروع و التفتيش / مساعد النائب",
        "الفرع الأوسط",
        "الفرع الغربي",
        "الفرع الشرقي",
        "الفرع الشمالي",
        "الفرع الجنوبي",
        "دعم التفتيش",
        "الفسح المركزي",
        "حوكمة وتطوير الفسح"
    ],
    "قطاع الأبحاث والمختبرات": [
        "مكتب القطاع",
        "الأبحاث والدراسات",
        "المختبرات",
        "المختبرات المرجعية",
        "المستحضرات الحيوية",
        "مركز تطوير المختبرات",
        "الشؤون التنظيمية لحلال",
        "الدعم والتنسيق"
    ],
    "قطاع رأس المال البشري": [
        "التطوير التنظيمي",
        "عمليات الموارد البشرية",
        "الإستقطاب وتطوير المواهب",
        "التوطين",
        "أكاديمية الغذاء والدواء"
    ],
    "قطاع الشؤون التنفيذية": [
        "التعاون الدولي",
        "الإتصال المؤسسي",
        "الحوكمة والمخاطر والإلتزام",
        "الأمن السيبراني"
    ],
    "قطاع التخطيط والتميز": [
        "التخطيط الإستراتيجي والبرامج",
        "التميز المؤسسي",
        "تنمية الإستثمار",
        "الاستطلاعات والتقارير",
        "مكتب إدارة البيانات"
    ],
    "قطاع الخدمات المساندة": [
        "الشؤون الهندسية والمرافق",
        "المشتريات والمواد",
        "الشؤون المالية",
        "التحول الرقمي وتقنية المعلومات",
        "مركز الوثائق والمحفوظات",
        "الاتصالات الإدارية"
    ],

    "لايوجد": [
        "مكتب الرئيس التنفيذي",
        "اللجنة الوطنية للتغذية",
        "الشؤون القانونية",
        "المراجعة الداخلية"
    ]
};

const sectorSelect = document.getElementById('sector');
const departmentSelect = document.getElementById('department');

function updateDepartments() {
    const selectedSector = sectorSelect.value;
   
    departmentSelect.innerHTML = '<option value="">اختر الإدارة</option>';

    if (selectedSector && sectorsAndDepartments[selectedSector]) {
        const departments = sectorsAndDepartments[selectedSector];
        departments.forEach(department => {
            const option = document.createElement('option');
            option.value = department;
            option.textContent = department;
            departmentSelect.appendChild(option);
        });
    }
}

// 1. استدعاء الدالة عند تغيير قيمة قائمة القطاع
sectorSelect.addEventListener('change', updateDepartments);

// 2. استدعاء الدالة عند تحميل الصفحة لتهيئة القائمة
updateDepartments();