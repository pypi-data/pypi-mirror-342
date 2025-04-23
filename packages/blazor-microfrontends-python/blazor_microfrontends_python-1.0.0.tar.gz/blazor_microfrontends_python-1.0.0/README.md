# Blazor Microfrontends Python SDK

A Python SDK for integrating Python microfrontends with Blazor applications.

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the SDK:
```bash
pip install -e .
```

## Usage

### App Shell Configuration

1. Initialize an app shell:
```bash
blazor-mf appshell init --name "MyAppShell" --version "1.0.0"
```

2. Add a microfrontend to the app shell:
```bash
blazor-mf appshell add "my-microfrontend" "http://localhost:5000" "/my-path"
```

3. List all microfrontends:
```bash
blazor-mf appshell list
```

### Microfrontend Development

1. Initialize a new microfrontend:
```bash
blazor-mf microfrontend init --name "MyMicrofrontend" --version "1.0.0"
```

2. Add routes to your microfrontend:
```bash
blazor-mf microfrontend add-route "/dashboard" "DashboardComponent"
```

3. List all routes:
```bash
blazor-mf microfrontend list-routes
```

### Flask Integration

```python
from flask import Flask, render_template
from blazor_microfrontends import MicrofrontendApi, microfrontend_route

app = Flask(__name__)
api = MicrofrontendApi(__name__)

@microfrontend_route(api, "/dashboard", "DashboardComponent")
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Django Integration

```python
from django.shortcuts import render
from blazor_microfrontends import MicrofrontendApi, microfrontend_route

api = MicrofrontendApi(__name__)

@microfrontend_route(api, "/dashboard", "DashboardComponent")
def dashboard(request):
    return render(request, 'dashboard.html')
```

## Configuration

### App Shell Configuration (appshell.yaml)

```yaml
name: MyAppShell
version: 1.0.0
microfrontends:
  - name: dashboard
    url: http://localhost:5000
    path: /dashboard
  - name: profile
    url: http://localhost:5001
    path: /profile
```

### Microfrontend Configuration (microfrontend.json)

```json
{
  "name": "MyMicrofrontend",
  "version": "1.0.0",
  "routes": [
    {
      "path": "/dashboard",
      "component": "DashboardComponent"
    }
  ]
}
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

4. Run type checking:
```bash
mypy .
```

## License

MIT License 