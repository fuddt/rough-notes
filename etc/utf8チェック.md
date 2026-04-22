#include <windows.h>
#include <string>
#include <iostream>

// UTF-8 として妥当かどうかを検査する
bool is_valid_utf8(const std::string& s)
{
    if (s.empty())
    {
        return true;
    }

    int result = MultiByteToWideChar(
        CP_UTF8,
        MB_ERR_INVALID_CHARS,
        s.data(),
        static_cast<int>(s.size()),
        nullptr,
        0
    );

    return result != 0;
}