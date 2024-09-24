import json
from urllib.parse import parse_qs

async def app(scope, receive, send):
    if scope['type'] == 'http':
        path = scope['path']
        if scope['method'] == 'GET':
            if path == '/factorial':
                await factorial_handler(scope, receive, send)
            elif path.startswith('/fibonacci'):
                await fibonacci_handler(scope, receive, send)
            elif path == '/mean':
                await mean_handler(scope, receive, send)
            else:
                await not_found(send)
        else:
            await not_found(send)

async def factorial_handler(scope, receive, send):
    query_string = scope['query_string'].decode('utf-8')
    query_params = parse_qs(query_string)

    if 'n' not in query_params or not query_params['n'][0].lstrip('-').isdigit():
        await send({
            'type': 'http.response.start',
            'status': 422,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Unprocessable Entity'}).encode('utf-8'),
        })
        return

    n = int(query_params['n'][0])

    if n < 0:
        await send({
            'type': 'http.response.start',
            'status': 400,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Bad Request: n must be non-negative'}).encode('utf-8'),
        })
        return

    result = {'result': factorial(n)}

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(result).encode('utf-8'),
    })

async def fibonacci_handler(scope, receive, send):
    path = scope['path']
    try:
        n = int(path.split('/')[-1])
    except ValueError:
        await send({
            'type': 'http.response.start',
            'status': 422,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Unprocessable Entity'}).encode('utf-8'),
        })
        return

    if n < 0:
        await send({
            'type': 'http.response.start',
            'status': 400,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Bad Request: n must be non-negative'}).encode('utf-8'),
        })
        return

    result = {'result': fibonacci(n)}

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(result).encode('utf-8'),
    })

async def mean_handler(scope, receive, send):
    body = await receive()

    if not body.get('body'):
        await send({
            'type': 'http.response.start',
            'status': 422,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Unprocessable Entity: no data provided'}).encode('utf-8'),
        })
        return

    data = json.loads(body.get('body').decode('utf-8'))

    if not isinstance(data, list) or len(data) == 0:
        await send({
            'type': 'http.response.start',
            'status': 400,
            'headers': [(b'content-type', b'application/json')],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Bad Request: expected a non-empty list'}).encode('utf-8'),
        })
        return

    result = sum(data) / len(data)

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({'result': result}).encode('utf-8'),
    })

async def not_found(send):
    await send({
        'type': 'http.response.start',
        'status': 404,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({'error': 'Not found'}).encode('utf-8'),
    })

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
