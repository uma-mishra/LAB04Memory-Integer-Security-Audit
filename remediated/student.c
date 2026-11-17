#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_NAME 32

typedef struct {
    char *name;
    int *marks;
    size_t count;
} Student;

Student *create_student(const char *name, size_t count)
{
    if (!name || strlen(name) > MAX_NAME ||
        count > SIZE_MAX / sizeof(int))
        return NULL;

    Student *s = calloc(1, sizeof(Student));
    if (!s) return NULL;

    s->name = malloc(strlen(name) + 1);
    if (!s->name) {
        free(s);
        return NULL;
    }

    strcpy(s->name, name);

    if (count > 0) {
        s->marks = calloc(count, sizeof(int));
        if (!s->marks) {
            free(s->name);
            free(s);
            return NULL;
        }
    }

    s->count = count;
    return s;
}

bool calculate_total(const Student *s, long long *result)
{
    if (!s || !result) return false;

    long long total = 0;

    for (size_t i = 0; i < s->count; i++) {
        if ((s->marks[i] > 0 && total > LLONG_MAX - s->marks[i]) ||
            (s->marks[i] < 0 && total < LLONG_MIN - s->marks[i]))
            return false;

        total += s->marks[i];
    }

    *result = total;
    return true;
}

bool add_bonus(Student *s, int bonus)
{
    if (!s) return false;

    for (size_t i = 0; i < s->count; i++) {
        if ((bonus > 0 && s->marks[i] > INT_MAX - bonus) ||
            (bonus < 0 && s->marks[i] < INT_MIN - bonus))
            return false;
    }

    for (size_t i = 0; i < s->count; i++)
        s->marks[i] += bonus;

    return true;
}

bool resize_marks(Student *s, size_t new_count)
{
    if (!s || new_count > SIZE_MAX / sizeof(int))
        return false;

    if (new_count == 0) {
        free(s->marks);
        s->marks = NULL;
        s->count = 0;
        return true;
    }

    int *temp = realloc(s->marks, new_count * sizeof(int));
    if (!temp) return false;

    for (size_t i = s->count; i < new_count; i++)
        temp[i] = 0;

    s->marks = temp;
    s->count = new_count;
    return true;
}

void display_student(const Student *s)
{
    if (!s) return;

    printf("Student: %s\n", s->name);

    for (size_t i = 0; i < s->count; i++)
        printf("Mark[%zu] = %d\n", i, s->marks[i]);
}

void destroy_student(Student *s)
{
    if (!s) return;

    free(s->name);
    free(s->marks);
    free(s);
}

int main(void)
{
    Student *student = create_student("Alice", 5);
    if (!student) return EXIT_FAILURE;

    const int marks[] = {80, 75, 90, 85, 95};

    for (size_t i = 0; i < 5; i++)
        student->marks[i] = marks[i];

    display_student(student);

    long long total;
    if (!calculate_total(student, &total)) {
        destroy_student(student);
        return EXIT_FAILURE;
    }

    printf("Total = %lld\n", total);

    if (!add_bonus(student, 5) ||
        !resize_marks(student, 10)) {
        destroy_student(student);
        return EXIT_FAILURE;
    }

    display_student(student);

    destroy_student(student);
    student = NULL;

    return EXIT_SUCCESS;
}
