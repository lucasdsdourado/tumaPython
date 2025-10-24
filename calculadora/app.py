from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
            backdrop-filter: blur(10px);
        }

        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 20px;
            font-size: 28px;
            font-weight: 600;
        }

        .calculator {
            display: grid;
            gap: 12px;
        }

        .display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 20px;
            border-radius: 15px;
            text-align: right;
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 10px;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            word-wrap: break-word;
            word-break: break-all;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        button {
            padding: 25px;
            font-size: 1.4em;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        button:active {
            transform: translateY(0);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        .number, .operator, .decimal {
            background: white;
            color: #333;
        }

        .operator {
            background: #f0f0f0;
            color: #667eea;
            font-weight: 600;
        }

        .equals {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            grid-column: span 2;
            font-weight: 600;
        }

        .clear {
            background: #ff6b6b;
            color: white;
            grid-column: span 2;
            font-weight: 600;
        }

        .clear:hover {
            background: #ff5252;
        }

        .equals:hover {
            opacity: 0.9;
        }

        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }

            .display {
                font-size: 2em;
                padding: 20px 15px;
            }

            button {
                padding: 20px;
                font-size: 1.2em;
            }

            h1 {
                font-size: 24px;
            }
        }

        .history {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.4em;
            margin-bottom: 5px;
            min-height: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Calculadora</h1>
        <div class="calculator">
            <div class="display">
                <div style="width: 100%;">
                    <div class="history" id="history"></div>
                    <div id="display">0</div>
                </div>
            </div>
            <div class="buttons">
                <button class="clear" onclick="clearDisplay()">C</button>
                <button class="operator" onclick="appendOperator('/')">&divide;</button>
                <button class="operator" onclick="appendOperator('*')">&times;</button>
                
                <button class="number" onclick="appendNumber('7')">7</button>
                <button class="number" onclick="appendNumber('8')">8</button>
                <button class="number" onclick="appendNumber('9')">9</button>
                <button class="operator" onclick="appendOperator('-')">-</button>
                
                <button class="number" onclick="appendNumber('4')">4</button>
                <button class="number" onclick="appendNumber('5')">5</button>
                <button class="number" onclick="appendNumber('6')">6</button>
                <button class="operator" onclick="appendOperator('+')">+</button>
                
                <button class="number" onclick="appendNumber('1')">1</button>
                <button class="number" onclick="appendNumber('2')">2</button>
                <button class="number" onclick="appendNumber('3')">3</button>
                <button class="equals" onclick="calculate()" style="grid-row: span 2;">=</button>
                
                <button class="number" onclick="appendNumber('0')" style="grid-column: span 2;">0</button>
                <button class="decimal" onclick="appendNumber('.')">.</button>
            </div>
        </div>
    </div>

    <script>
        let currentValue = '0';
        let previousValue = '';
        let operation = '';
        let shouldResetDisplay = false;

        const display = document.getElementById('display');
        const history = document.getElementById('history');

        function updateDisplay() {
            display.textContent = currentValue;
            if (previousValue && operation) {
                history.textContent = `${previousValue} ${operation}`;
            } else {
                history.textContent = '';
            }
        }

        function appendNumber(num) {
            if (shouldResetDisplay) {
                currentValue = num;
                shouldResetDisplay = false;
            } else {
                if (currentValue === '0' && num !== '.') {
                    currentValue = num;
                } else if (num === '.' && currentValue.includes('.')) {
                    return;
                } else {
                    currentValue += num;
                }
            }
            updateDisplay();
        }

        function appendOperator(op) {
            if (previousValue && operation && !shouldResetDisplay) {
                calculate();
            }
            operation = op;
            previousValue = currentValue;
            shouldResetDisplay = true;
            updateDisplay();
        }

        function calculate() {
            if (!previousValue || !operation) return;

            const prev = parseFloat(previousValue);
            const current = parseFloat(currentValue);
            let result;

            switch(operation) {
                case '+':
                    result = prev + current;
                    break;
                case '-':
                    result = prev - current;
                    break;
                case '*':
                    result = prev * current;
                    break;
                case '/':
                    if (current === 0) {
                        currentValue = 'Erro';
                        previousValue = '';
                        operation = '';
                        updateDisplay();
                        shouldResetDisplay = true;
                        return;
                    }
                    result = prev / current;
                    break;
                default:
                    return;
            }

            currentValue = result.toString();
            if (currentValue.length > 12) {
                currentValue = parseFloat(currentValue).toExponential(6);
            }
            
            previousValue = '';
            operation = '';
            shouldResetDisplay = true;
            updateDisplay();
        }

        function clearDisplay() {
            currentValue = '0';
            previousValue = '';
            operation = '';
            shouldResetDisplay = false;
            updateDisplay();
        }

        // Suporte a teclado
        document.addEventListener('keydown', function(event) {
            if (event.key >= '0' && event.key <= '9' || event.key === '.') {
                appendNumber(event.key);
            } else if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') {
                appendOperator(event.key);
            } else if (event.key === 'Enter' || event.key === '=') {
                calculate();
            } else if (event.key === 'Escape' || event.key === 'c' || event.key === 'C') {
                clearDisplay();
            }
        });

        updateDisplay();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

