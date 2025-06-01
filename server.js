const express = require('express');
const bodyParser = require('body-parser');
// const bcrypt = require('bcrypt'); // Для хешування паролів
// const jwt = require('jsonwebtoken'); // Для створення токенів

const app = express();
const port = 3000;

app.use(bodyParser.json());

// Псевдо-функція для підключення до бази даних
function connectToDatabase() {
    console.log('Підключення до бази даних...');
    // Тут має бути код для підключення до твоєї бази даних
}

// Псевдо-функція для перевірки існування користувача
async function userExists(username, email) {
    // Тут має бути запит до бази даних для перевірки
    return false; // Завжди повертає false для прикладу
}

// Псевдо-функція для хешування пароля
async function hashPassword(password) {
    // const saltRounds = 10;
    // return await bcrypt.hash(password, saltRounds);
    return password + '_hashed'; // Заглушка для прикладу! У production коді використовуй bcrypt!
}

// Псевдо-функція для створення нового користувача в базі даних
async function createUser(username, email, hashedPassword) {
    console.log('Створення користувача:', username, email, hashedPassword);
    // Тут має бути код для запису в базу даних
}

// Псевдо-функція для пошуку користувача за логіном (username або email)
async function findUser(login) {
    console.log('Пошук користувача за логіном:', login);
    // Тут має бути запит до бази даних
    return null; // Завжди повертає null для прикладу
}

// Псевдо-функція для порівняння пароля з хешем
async function verifyPassword(plainPassword, hashedPassword) {
    // return await bcrypt.compare(plainPassword, hashedPassword);
    return plainPassword + '_hashed' === hashedPassword; // Заглушка!
}

// Псевдо-функція для генерації токена авторизації (JWT)
function generateToken(username) {
    // return jwt.sign({ username }, 'your-secret-key', { expiresIn: '1h' });
    return 'fake_token_for_' + username; // Заглушка!
}

app.post('/api/register', async (req, res) => {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
        return res.status(400).json({ message: 'Будь ласка, заповніть всі поля.' });
    }

    if (await userExists(username, email)) {
        return res.status(409).json({ message: 'Користувач з таким ім\'ям або email вже існує.' });
    }

    const hashedPassword = await hashPassword(password);
    await createUser(username, email, hashedPassword);
    const token = generateToken(username);

    res.status(201).json({ message: 'Реєстрація успішна!', token: token });
});

app.post('/api/login', async (req, res) => {
    const { login, password } = req.body;

    if (!login || !password) {
        return res.status(400).json({ message: 'Будь ласка, введіть логін та пароль.' });
    }

    const user = await findUser(login);

    if (!user || !(await verifyPassword(password, user.password_hash))) {
        return res.status(401).json({ message: 'Невірний логін або пароль.' });
    }

    const token = generateToken(user.username);
    res.json({ token: token });
});

app.listen(port, () => {
    console.log(`Сервер запущено на http://localhost:${port}`);
    connectToDatabase();
});