# SketchMind frontend

React + TypeScript + Vite. Залежності зафіксовано в `package-lock.json`.

## Локальний запуск

Використовуй Node.js 22.19.0 (версія в `.nvmrc`) та npm.
Команди нижче виконуються з кореня репозиторію.

```powershell
cd frontend
npm ci
npm run dev
```

Frontend: http://localhost:5173. Якщо порт зайнятий, Vite повідомить про помилку.

## Підключення backend

В окремому терміналі з кореня репозиторію:

```powershell
dotnet run --project backend/SketchMind.Api --launch-profile http
```

Vite перенаправляє запити `/api/*` на `http://localhost:5260`, прибираючи
префікс `/api`. Наприклад, `fetch('/api/weatherforecast')` звертається
до наявного endpoint `/weatherforecast`. Проксі дозволяє працювати через
один origin у браузері без додаткового CORS-конфігу.

Щоб змінити адресу backend:

```powershell
cd frontend
Copy-Item .env.example .env.local
```

Зміни `API_PROXY_TARGET` у `.env.local` і перезапусти Vite.
Це серверне налаштування Vite. Змінні з префіксом `VITE_` потрапляють
у браузерний bundle, тому не зберігай у них секрети.

## Перевірки й збірка

Виконувати з `frontend`:

```powershell
npm run typecheck # TypeScript
npm run lint      # ESLint
npm run check     # ESLint + TypeScript + production build
npm run preview   # перегляд готової збірки після npm run build
```

Збірка зберігається в `dist/`. Dev-проксі не входить до production build:
на хостингу потрібно налаштувати `/api/*` на backend з таким самим видаленням
префікса. `npm run preview` також не проксіює API.

Імпорти `@/…` посилаються на `src/`; alias налаштовано у Vite та TypeScript.
Строгий режим TypeScript увімкнений для застосунку й конфігурації Vite.

Наразі застосунок містить мінімальний екран SketchMind. Предметні екрани та API
розпізнавання ще потрібно реалізувати. Спільний `.gitignore` розташований у корені
репозиторію й охоплює frontend, .NET backend та Python ML-сервіс.
