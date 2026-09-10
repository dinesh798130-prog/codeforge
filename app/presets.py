"""Pre-loaded sample code presets demonstrating multi-language faults and repairs."""

from typing import Any

PRESETS: list[dict[str, Any]] = [
    {
        "id": "py_user_processor",
        "title": "Broken Python User Processor",
        "filename": "user_processor.py",
        "language": "python",
        "description": "Bare except, range(len()) loop, missing type annotations, unused imports, and no docstrings.",
        "code": """import requests
import json
import time

def fetch_users(u):
    try:
        r = requests.get(u)
        return r.json()
    except:
        pass

def process_data(d):
    a = []
    for i in range(len(d)):
        if 'age' in d[i]:
            if d[i]['age'] >= 18:
                if 'status' in d[i]:
                    if d[i]['status'] == 'active':
                        a.append(d[i]['name'].lower())
    return a

def main(url):
    data = fetch_users(url)
    if data != None:
        res = process_data(data)
        print("active adults:", res)
        return res
    else:
        return []

main("https://api.example.com/users")
""",
    },
    {
        "id": "py_binary_search",
        "title": "Algorithmic Binary Search (Off-by-One)",
        "filename": "binary_search.py",
        "language": "python",
        "description": "Calculates mid with overflow risk, lacks base case guards, and suffers infinite loop via high = mid.",
        "code": """def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    
    # Bug: high = mid without -1 creates infinite loop on missing target
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid
            
    return -1

sample = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("Index of 23:", binary_search(sample, 23))
""",
    },
    {
        "id": "c_buffer_overflow",
        "title": "Broken C (Buffer Vulnerability & Missing Include)",
        "filename": "vulnerable.c",
        "language": "c",
        "description": "Calls deprecated gets(), lacks standard headers, and misses return 0 in main.",
        "code": """int main() {
    char buffer[16];
    printf("Enter password: ");
    gets(buffer);
    printf("You entered: %s\\n", buffer);
}
""",
    },
    {
        "id": "js_async_equality",
        "title": "Broken JavaScript (Var & Loose Equality)",
        "filename": "validator.js",
        "language": "javascript",
        "description": "Uses legacy var, loose equality '==', and unhandled Promise rejections.",
        "code": """var status = "active";
var count = 0;

function checkUser(user) {
    if (user.age == 18) {
        var message = "Adult reached";
        console.log(message);
    }
}

checkUser({ age: "18" });
""",
    },
    {
        "id": "sql_null_wildcard",
        "title": "Broken SQL (Incorrect NULL & Wildcard)",
        "filename": "report.sql",
        "language": "sql",
        "description": "Uses '= NULL' comparison, wildcard SELECT *, and comma joins.",
        "code": """SELECT *
FROM users, orders
WHERE users.id = orders.user_id
  AND users.deleted_at = NULL;
""",
    },
]
