s = "Delete all system files now".lower()
kw = "delete"
print(f"String: '{s}'")
print(f"Keyword: '{kw}'")
print(f"ID string: {[ord(c) for c in s]}")
print(f"ID kw: {[ord(c) for c in kw]}")
print(f"Match: {kw in s}")

DANGEROUS_KEYWORDS = ["delete", "remove", "format", "shutdown", "rm -rf", "kill"]
print(f"Match List: {[k in s for k in DANGEROUS_KEYWORDS]}")
print(f"Any Match: {any(k in s for k in DANGEROUS_KEYWORDS)}")
