# Lab 4 – Memory and Integer Security Audit

| No. | Function | Defect | Impact | Fix |
|---|---|---|---|---|
| 1 | create_student | Unchecked malloc | NULL pointer dereference | Check allocation |
| 2 | create_student | Missing NULL name validation | Invalid memory access | Validate input |
| 3 | create_student | Name length only warns | Overlong input accepted | Reject overlong names |
| 4 | create_student | malloc(strlen(name)) | Heap buffer overflow | Allocate strlen + 1 |
| 5 | create_student | Unchecked strcpy | Buffer overflow | Allocate sufficient memory |
| 6 | create_student | Negative int count | Invalid huge allocation | Use size_t |
| 7 | create_student | Multiplication overflow | Undersized allocation | Check SIZE_MAX |
| 8 | calculate_total | i <= count | Out-of-bounds read | Use i < count |
| 9 | calculate_total | int total | Integer overflow | Use long long and check |
| 10 | add_bonus | Unchecked addition | Signed integer overflow | Check INT_MIN and INT_MAX |
| 11 | resize_marks | Direct realloc assignment | Memory leak on failure | Use temporary pointer |
| 12 | resize_marks | Unchecked multiplication | Integer overflow | Validate size |
| 13 | resize_marks | New memory uninitialized | Uninitialized memory read | Initialize new elements |
| 14 | destroy_student | Double free of name | Heap corruption | Free once |
| 15 | main | Use after free | Undefined behaviour | Do not access freed object |
| 16 | Multiple functions | Missing NULL checks | Invalid memory access | Validate pointers |

## Verification Results

- GCC hardening compilation: Passed
- AddressSanitizer: No errors reported
- UBSan: No errors reported
- Valgrind: 0 errors, 0 bytes leaked
- cppcheck: No warnings after remediation

## Conclusion

The original program contained memory management, buffer overflow,
out-of-bounds access, integer overflow, and use-after-free defects.

The corrected program uses allocation checks, bounds validation,
safe resizing, overflow checks, proper cleanup, and compiler hardening.

All verification tools completed successfully on the corrected program.
