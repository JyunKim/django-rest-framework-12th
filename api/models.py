from django.db import models
from django.contrib.auth.models import User
# manage.py makemigrations --name filename appname


class Lecture(models.Model):
    # related_name - objects와 같음 => all(), create() 등 사용 가능
    # pk는 string 보다 integer로 하는게 용량 상 좋음
    # 첫번째 인자로 verbose_name -> 어드민 사이트에서 변수 이름 대신 사용
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE, related_name='lectures', verbose_name='담당교수')
    code = models.CharField('학정번호', max_length=30)
    faculty = models.CharField('학부대학', max_length=30)
    department = models.CharField('전공', max_length=30)
    semester = models.CharField('학기', max_length=30)
    grade = models.IntegerField('학년')
    name = models.CharField('교과목명', max_length=30)
    credit = models.IntegerField('학점')
    classroom = models.CharField('강의실', max_length=50)
    time = models.CharField('강의시간', max_length=50)

    def __str__(self):
        return "{}, {}".format(self.name, self.professor.name)


class Professor(models.Model):
    # null=True면 blank=True여야 함
    name = models.CharField('이름', max_length=30)
    department = models.CharField('소속', max_length=30, null=True, blank=True)
    office = models.CharField('연구실', max_length=30, null=True, blank=True)
    phone = models.CharField('연락처', max_length=30, null=True, blank=True)
    email = models.EmailField('이메일', null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.department)


class Rank(models.Model):
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='ranks', verbose_name='과목')
    mileage = models.IntegerField('마일리지')
    is_major = models.BooleanField('전공 여부')
    is_included = models.BooleanField('전공자 정원 포함 여부')
    grade = models.IntegerField('학년')
    success = models.BooleanField('수강 여부')


class Result(models.Model):
    lecture = models.OneToOneField('Lecture', on_delete=models.CASCADE, verbose_name='과목')
    quota = models.IntegerField('정원')
    participants = models.IntegerField('참여 인원')
    major_quota = models.IntegerField('전공자 정원')
    include_second_major = models.BooleanField('복수전공 포함 여부')
    max_mileage = models.IntegerField('최대 마일리지')


class Major(models.Model):
    name = models.CharField('학과명', max_length=30)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lectures = models.ManyToManyField(Lecture, related_name='users')
    student_id = models.IntegerField('학번', unique=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='users', verbose_name='전공')
    second_major = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name='second_users',
                                     verbose_name='복수전공', null=True, blank=True)
    grade = models.IntegerField('학년')
    created_at = models.DateTimeField('가입일시', auto_now_add=True)
    updated_at = models.DateTimeField('변경일시', auto_now=True)

    def __str__(self):
        return self.user.username
