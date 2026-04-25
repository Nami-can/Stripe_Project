#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' 

clear
echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                      ║${NC}"
echo -e "${CYAN}║              ${GREEN}STRIPE${CYAN}                  ║${NC}"
echo -e "${CYAN}║                                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
echo ""

while true; do
    echo -e "${YELLOW}Выберите действие:${NC}"
    echo ""
    echo "  1   Установить зависимости requirements.txt"
    echo "  2   Сделать миграцию"
    echo "  3   Создать суперпользователя"
    echo "  4   Запустить сервер"
    echo "  5   Сменить Stripe ключи"
    echo "  6   Создать тестовый товар"
    echo "  0   Выход"
    echo ""
    read -p "Введите номер: " choice
    
    case $choice in

        1)   
            echo -e "${YELLOW}Установка зависимостей:${NC}"
            pip install -r requirements.txt

            echo -e "${YELLOW}Успешно завершено!"
            echo ""
            ;; 

        2)   
            echo -e "${YELLOW}Начало миграции:${NC}"
            python manage.py makemigrations
            python manage.py migrate

            echo -e "${YELLOW}Успешно завершено!"
            echo ""
            ;; 

        3)
            echo -e "${YELLOW}Создание суперпользователя:${NC}"
            python manage.py createsuperuser
            echo ""
            ;;
        
        4)
            echo -e "${GREEN}▶ Запускаем сервер...${NC}"
            echo -e "${YELLOW}Сервер запущен на http://127.0.0.1:8000/${NC}"
            echo -e "${YELLOW}Админка: http://127.0.0.1:8000/admin/${NC}"
            echo -e "${YELLOW}Ctrl+C для остановки${NC}"
            echo ""
            python manage.py runserver
            ;;
        5)
            echo ""
            echo -e "${YELLOW}Введите новые ключи Stripe:${NC}"
            read -p "Publishable Key (pk_test_...): " pk
            read -p "Secret Key (sk_test_...): " sk
            
            sed -i "s/STRIPE_PUBLIC_KEY=.*/STRIPE_PUBLIC_KEY=$pk/" .env
            sed -i "s/STRIPE_SECRET_KEY=.*/STRIPE_SECRET_KEY=$sk/" .env
            
            echo -e "${GREEN}Ключи обновлены!${NC}"
            echo ""
            ;;
        6)
            echo ""
            echo -e "${YELLOW}Создание тестового товара...${NC}"
            python manage.py shell << 'PYEOF'
from shop.models import Item
item = Item.objects.create(
    name="Тестовый товар",
    description="Описание тестового товара",
    price=100.00,
    currency="rub"
)
print(f"Товар создан! ID: {item.id}")
PYEOF
            echo ""
            ;;
        

        
        0)
            echo -e "${RED}Пока!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Неверный выбор${NC}"
            echo ""
            ;;
    esac
done
