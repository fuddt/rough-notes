#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

// 1つの再生区間を表す構造体
struct Segment
{
    int startFrame;
    int endFrame;   // [startFrame, endFrame) の終端。endFrame 自体は再生しない
};

// セグメント一覧をファイルから読み込む関数
std::vector<Segment> loadSegments(const std::string& filePath)
{
    std::ifstream ifs(filePath);
    if (!ifs)
    {
        throw std::runtime_error("セグメント定義ファイルを開けませんでした: " + filePath);
    }

    std::vector<Segment> segments;
    std::string line;
    int lineNumber = 0;

    // 1行ずつ読む
    while (std::getline(ifs, line))
    {
        ++lineNumber;

        // 前後に空白があっても istringstream 側で吸収される
        // まず空行やコメント行を処理する
        if (line.empty())
        {
            continue;
        }

        // 行頭が # ならコメントとして無視
        if (!line.empty() && line[0] == '#')
        {
            continue;
        }

        std::istringstream iss(line);

        Segment seg{};

        // "500 1000" のような2整数を読む
        if (!(iss >> seg.startFrame >> seg.endFrame))
        {
            throw std::runtime_error(
                "フォーマット不正です。行 " + std::to_string(lineNumber) +
                ": \"" + line + "\"");
        }

        // 余計なゴミが後ろにないか確認する
        // 例: "500 1000 abc" は不正として落とす
        std::string extra;
        if (iss >> extra)
        {
            throw std::runtime_error(
                "余計なトークンがあります。行 " + std::to_string(lineNumber) +
                ": \"" + line + "\"");
        }

        // 妥当性チェック
        if (seg.startFrame < 0)
        {
            throw std::runtime_error(
                "startFrame は 0 以上である必要があります。行 " +
                std::to_string(lineNumber));
        }

        if (seg.endFrame <= seg.startFrame)
        {
            throw std::runtime_error(
                "endFrame は startFrame より大きい必要があります。行 " +
                std::to_string(lineNumber));
        }

        segments.push_back(seg);
    }

    if (segments.empty())
    {
        throw std::runtime_error("有効なセグメントが1件もありません");
    }

    return segments;
}