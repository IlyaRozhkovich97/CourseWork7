from rest_framework import serializers
from habit.models import Habits
from habit.validators import HabitsDurationValidator, HabitsPeriodicValidator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели `Habits`.

    Этот сериализатор используется для создания, обновления и получения данных о привычках.
    Он включает в себя следующие проверки и валидации:

    1. **Приятные привычки**:
       - Не могут иметь вознаграждение или связанную привычку.
       - Если привычка отмечена как приятная (`is_nice=True`), поля `prize` и `related` должны быть пустыми.

    2. **Связанные привычки**:
       - Связанная привычка (`related`) должна быть также приятной (`is_nice=True`).

    3. **Вознаграждение и связанная привычка**:
       - Нельзя указывать одновременно и вознаграждение (`prize`), и связанную привычку (`related`).

    4. **Дни недели**:
       - Должен быть выбран хотя бы один день недели из списка (`sunday`, `monday`, `tuesday`, `wednesday`,
       `thursday`, `friday`, `saturday`).

    Валидация времени выполнения и периодичности привычки осуществляется через кастомные валидаторы, указанные в
    `Meta` классе.
    """

    class Meta:
        model = Habits
        fields = "__all__"
        validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]

    def validate(self, data):
        """
        Выполняет пользовательскую валидацию данных.

        Проверяет следующие условия:

        - Не может быть указано одновременно `related` и `prize`.
        - Если привычка является приятной (`is_nice=True`), то не может иметь `related` или `prize`.
        - Если указана связанная привычка (`related`), она должна быть приятной.
        - Должен быть выбран хотя бы один день недели.

        :param data: Словарь данных о привычке.
        :type data: dict
        :raises serializers.ValidationError: В случае нарушения правил валидации.
        :return: Очищенный и валидированный словарь данных.
        :rtype: dict
        """

        # Проверка: либо связанная привычка, либо вознаграждение
        if data.get("related") and data.get("prize"):
            raise serializers.ValidationError(
                "Может быть указано либо вознаграждение, либо связанная привычка, но не оба одновременно.")

        # Проверка: приятная привычка не может иметь связанную привычку или вознаграждение
        if data.get("is_nice"):
            if data.get("related") or data.get("prize"):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки или вознаграждения.")

        # Проверка: связанная привычка должна быть приятной
        related_habit = data.get("related")
        if related_habit and not related_habit.is_nice:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        # Проверка: хотя бы один день недели должен быть выбран
        days_of_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        if not any(data.get(day) for day in days_of_week):
            raise serializers.ValidationError("Хотя бы один день в неделю должен быть выбран!")

        # Периодичность и длительность проверяются валидаторами
        periodicity_validator = HabitsPeriodicValidator(field="periodicity")
        duration_validator = HabitsDurationValidator(field="duration")

        periodicity_validator(data)
        duration_validator(data)

        return data
