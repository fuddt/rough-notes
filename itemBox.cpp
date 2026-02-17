#include <iostream>
#include <string>
#include <vector>
#include <optional>

// アイテム。まずは「名前」だけで十分。
// 後で「種類」「スタック可能」「個数」などを拡張する。
struct Item {
    std::string name;
};

// アイテムBOX本体（共有される実体）
// - 所有: items_ がアイテムを保持（寿命はItemBoxに従う）
// - 容量制限: capacity_
class ItemBox {
public:
    explicit ItemBox(std::size_t capacity)
        : capacity_(capacity) {}

    // 入れる：成功したらtrue、満杯ならfalse
    bool deposit(Item item) {
        if (items_.size() >= capacity_) return false;
        items_.push_back(std::move(item)); // ここは深追い不要。とりあえず「入れる」意味。
        return true;
    }

    // 取り出す：名前で探して取り出す（見つからなければnullopt）
    std::optional<Item> withdrawByName(const std::string& name) {
        for (std::size_t i = 0; i < items_.size(); ++i) {
            if (items_[i].name == name) {
                Item out = std::move(items_[i]);      // 取り出すアイテム
                items_.erase(items_.begin() + i);      // BOXから消す
                return out;
            }
        }
        return std::nullopt;
    }

    void print() const {
        std::cout << "[ItemBox] " << items_.size() << "/" << capacity_ << "\n";
        for (const auto& it : items_) {
            std::cout << " - " << it.name << "\n";
        }
    }

private:
    std::size_t capacity_;
    std::vector<Item> items_; // ItemBoxが所有する（第1章の主役）
};

// 部屋：BOXを「所有しない」
// ここが重要。部屋は共有BOXにアクセスするだけ。
class Room {
public:
    Room(std::string name, ItemBox& sharedBox)
        : name_(std::move(name)), box_(sharedBox) {}

    void put(Item item) {
        const bool ok = box_.deposit(std::move(item));
        std::cout << "[" << name_ << "] put -> " << (ok ? "OK" : "FULL") << "\n";
    }

    void take(const std::string& itemName) {
        auto got = box_.withdrawByName(itemName);
        if (!got) {
            std::cout << "[" << name_ << "] take -> NOT FOUND\n";
            return;
        }
        std::cout << "[" << name_ << "] take -> " << got->name << "\n";
    }

    void showBox() const {
        std::cout << "[" << name_ << "] show box\n";
        box_.print();
    }

private:
    std::string name_;
    ItemBox& box_; // 参照: 「必ず存在する共有BOX」を借りる設計
};

int main() {
    ItemBox sharedBox(5);

    Room hall("Hall", sharedBox);
    Room lab("Lab", sharedBox);

    hall.put(Item{"Handgun"});
    hall.put(Item{"Herb"});
    lab.showBox();             // 別の部屋でも同じ中身が見える

    lab.take("Handgun");       // Labで取り出す
    hall.showBox();            // Hallから見ると消えている
}