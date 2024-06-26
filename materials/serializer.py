from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Класс создания сериализатора для модели Lesson"""

    class Meta:
        model = Lesson
        fields = "__all__"  # Или кортеж полей, которые необходимо вывести


class CourseSerializer(ModelSerializer):
    """Класс создания сериализатора для модели Course"""

    class Meta:
        model = Course
        fields = "__all__"   # Или кортеж полей, которые необходимо вывести


class CourseDetailSerializer(ModelSerializer):
    """Класс создания сериализатора для модели Course"""
    # Задаем новое поле для модели. которое будет передаваться через Serializer
    count_lessons_for_course = SerializerMethodField()
    # Получаем новое поле для модели. которое будет передаваться через Serializer
    # Обращаюсь через lessons, а не lesson_set, так как в модели настроен related_name
    # lessons = LessonSerializer(source='lessons', many=True, read_only=True)

    # Излишним указывать `source='lessons'` в поле ListSerializer в сериализаторе CourseSerializer,
    # поскольку оно совпадает с именем поля.
    # При использовании сериализатора для связанной модели LessonSerializer
    # read_only=True означает, что открыт только для чтения, write_only=True - можно будет записывать,
    # но откроются все поля для заполнения
    lessons = LessonSerializer(many=True, read_only=True)

    # Вариант выведения lessons с использованием SerializerMethodField()
    # lessons = SerializerMethodField()
    #
    # def get_lessons(self, course):
    #     """Метод для получения списка назвпний уроков"""
    #     lessons = [lesson.name for lesson in Lesson.objects.filter(course=course)]
    #
    #     return lessons

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_count_lessons_for_course(course):
        """Метод для получения количества уроков, входящих в курс"""

        return course.lessons.count()
