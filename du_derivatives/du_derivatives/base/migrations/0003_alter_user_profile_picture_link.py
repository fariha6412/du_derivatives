# Generated by Django 4.1.7 on 2023-04-13 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_user_id_user_csedu_batch_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture_link',
            field=models.CharField(default='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIIAAACCCAMAAAC93eDPAAAAM1BMVEXFxcX////CwsLLy8v09PT8/PzIyMjPz8/q6urw8PDX19fd3d3j4+Pn5+fg4ODt7e27u7u9ms3EAAAC4ElEQVR4nO2a3XKjMAyFbYMxEFL6/k+7uJRNGlIsHY6yna6/i07vckboX3auUqlUKpVKpVKp/C+EELomLTTd8v8/+H3XjH0bY/R++dPOl8a9VkXoptY/0F7T62wRxuHx9z9VXF5jipC+EZCJo72I4K7fC8gMjbGGkOKxgoXRVEO4FAUs9IYawiRRsHwMOwUFN7jRGtkhvEkVeD/bKBD5wYaFP0hi4Z4LX0PQKfC+oysQBsMNuks2WgX0FBVmvYSW+ymSXoH3b0wzhB6RQPWGThsOKyNPQRghBcz8hDjjB0QJoAKfaAqgeMhMLDNoSuRXZpoEKCQzLUmBcwct8zGRliB3Y4uY5vdIAHNjlcCW8AN8waElgheU8hHmEVpq0k0Q99ASNNa2ZXitG1ysad4ItyyR2LKAzkAdLLHkRGuaHDLOZbgjHRQT3OEaaZx4LdMnegmJPFrrg4KXGf9q0JZL+opj6Rp0CiwWoLrBkjbEwBp6CwFOM1UNZitgaViYLqFHSbGgLnj2GppibEZ2StqLKDjE3Nnfht67A0PE9G5uA5f6Q3eIfTK9ToXD09jGYHgsDKOwTrRG5ymRBe4sYSBhUvWPcWL/viAf7L4G92CJdfHU3hEcZXhHsg7euA2k1ukoG5agnEVCg695FiLBKc8pyBpOKzjxFVbasxpOKzg7VamHh+caTrgDvuf6yhXWgJ6k9sCV82ww3EDDguMIK5g74OegZ0CNvXKMLQFk6gDXpufoZzxeNGzoo4LoiyvaJMn1xRWlR6pfrgjQrYMtjKA0g4URdGbgh8OKJijIOWFD8fwOvsKUEK/mWW3CHnHjcOI0WkB8NDRyxozwjQ/+YqKMcB0I3+MkiCTgj2ckiFYf2B1Kimg9zmwZ98iaSLOQzESJAlNXECVI/EwvQ7D9scwKGUlmMPVGUQtpVyBWBGXC2Bsl/vgDJBiWyZVisbTpne8p9tF2HdNGsXOCX9qK2Z3T/wC1CiK7mFWvswAAAABJRU5ErkJggg==', max_length=300, null=True),
        ),
    ]