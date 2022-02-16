#include <windows.h>

int main(void)
{
    MessageBox(NULL, L"test", L"test", 0x20);
    Sleep(2000);
    MessageBox(NULL, L"test2", L"test2", 0x06);
    return 0;
}