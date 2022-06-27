#include <list>
#include <iostream>
#include <queue>
#include <deque>

using namespace std;

extern "C"
{
    void detect_rectangles(unsigned char *image, int rows, int cols, int *l_limit, int *h_limit, int *rectangles, int *size)
    {
        queue<int> q;
        int cnt = 0;
        int min_r, min_c, max_r, max_c;
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                if (*(image + i * cols + j))
                {
                    q.push(i * cols + j);
                    min_r = max_r = i;
                    min_c = max_c = j;
                    while (!q.empty())
                    {
                        int idx = q.front();
                        q.pop();
                        int row = idx / cols;
                        int col = idx % cols;
                        if ((row < 0 || col < 0 || row >= rows || col >= cols) || *(image + row * cols + col) == 0)
                            continue;

                        *(image + row * cols + col) = 0;
                        if (min_r > row)
                            min_r = row;
                        if (max_r < row)
                            max_r = row;
                        if (min_c > col)
                            min_c = col;
                        if (max_c < col)
                            max_c = col;
                        q.push((row + 1) * cols + col);
                        q.push((row - 1) * cols + col);
                        q.push(row * cols + col + 1);
                        q.push(row * cols + col - 1);
                    }
                    rectangles[cnt++] = min_r;
                    rectangles[cnt++] = min_c;
                    rectangles[cnt++] = max_r;
                    rectangles[cnt++] = max_c;
                    if (cnt == *size)
                        return;
                }
        *size = cnt;
    }
}

int main()
{
    return 0;
}