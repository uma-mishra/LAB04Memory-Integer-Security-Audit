# Unit I Practical Assignment
# Memory and Integer Security Audit

## 1. Defect Table

| No. | Exact Location | Defect Type | Security Impact | Remediation |
|---|---|---|---|---|
| 1 | Line 16 – create_student | Unchecked malloc | NULL pointer dereference | Check allocation result |
| 2 | Line 17 – create_student | Missing NULL input validation | Invalid memory access in strlen | Reject NULL name |
| 3 | Lines 17–18 – create_student | Improper input validation | Overlong names are accepted | Reject names exceeding MAX_NAME |
| 4 | Line 19 – create_student | Insufficient allocation | Missing space for null terminator | Allocate strlen(name) + 1 |
| 5 | Line 20 – create_student | Unsafe strcpy / heap buffer overflow | Heap memory corruption | Allocate sufficient memory and validate input |
| 6 | Lines 14, 21–22 – create_student | Negative count / signed-to-unsigned conversion | Invalid allocation size and excessive memory request | Use size_t and validate count |
| 7 | Line 22 – create_student | Integer overflow in allocation multiplication | Undersized allocation and possible buffer overflow | Check SIZE_MAX before multiplication |
| 8 | Lines 16, 19, 22 – create_student | Unchecked memory allocations | NULL pointer dereference | Check every allocation |
| 9 | Line 29 – calculate_total | Off-by-one error | Out-of-bounds array read | Use i < s->count |
| 10 | Line 30 – calculate_total | Signed integer overflow | Undefined behaviour and incorrect total | Use checked wider arithmetic |
| 11 | Lines 29–30 – calculate_total | Signed/unsigned index mismatch | Incorrect boundary handling | Use size_t indices |
| 12 | Line 37 – add_bonus | Signed integer overflow | Undefined behaviour and corrupted marks | Check INT_MIN and INT_MAX |
| 13 | Line 37 – add_bonus | Missing pointer validation | Invalid memory access | Validate student pointer |
| 14 | Line 42 – resize_marks | Direct realloc assignment | Original allocation can be lost on failure | Use a temporary pointer |
| 15 | Line 42 – resize_marks | Allocation-size multiplication overflow | Undersized allocation | Validate count against SIZE_MAX |
| 16 | Lines 40–43 – resize_marks | Negative count / signed-to-unsigned conversion | Invalid resize size | Use size_t and validate input |
| 17 | Lines 42–43 – resize_marks | Uninitialized newly allocated elements | Uninitialized memory reads | Initialize newly added elements |
| 18 | Lines 46–50 – display_student | Missing NULL pointer validation | Invalid memory access | Validate student pointer |
| 19 | Lines 55–57 – destroy_student | Double free of name | Heap corruption and undefined behaviour | Free name only once |
| 20 | Lines 53–58 – destroy_student | Missing NULL pointer validation | Invalid memory access | Check pointer before cleanup |
| 21 | Lines 79–80 – main | Use-after-free | Undefined behaviour and possible information disclosure | Do not access object after destruction |
| 22 | Line 64 and subsequent main operations | Unchecked create_student result | NULL pointer dereference | Check returned pointer |

## 2. Remediation Summary

- Checked all dynamic memory allocations.
- Added NULL pointer validation.
- Allocated sufficient space for string terminators.
- Replaced unsafe allocation-size calculations with range checks.
- Corrected array loop boundaries.
- Added integer overflow checks.
- Used temporary pointers for realloc.
- Initialized newly allocated array elements.
- Removed duplicate free operations.
- Removed use-after-free access.
- Used size_t for array counts and indices.
- Added compiler hardening options.

## 3. Verification Results

| Tool | Result |
|---|---|
| GCC hardening compilation | Passed |
| AddressSanitizer | No errors reported |
| UndefinedBehaviorSanitizer | No errors reported |
| Valgrind Memcheck | 0 errors |
| Valgrind memory leaks | 0 bytes |
| cppcheck | No warnings after remediation |

## 4. Conclusion

The original faculty module contained memory management errors,
unsafe string handling, out-of-bounds access, integer overflow,
allocation-size errors, double-free and use-after-free defects.

The remediated implementation introduces checked allocations,
correct initialization, safe resizing, range-checked arithmetic,
and correct memory cleanup.

The corrected module was tested using GCC, AddressSanitizer,
UndefinedBehaviorSanitizer, Valgrind and cppcheck.
