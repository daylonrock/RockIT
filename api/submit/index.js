module.exports = async function (context, req) {
    context.log('Contact form API triggered.');

    let body = req.body;
    if (typeof body === 'string') {
        try {
            body = JSON.parse(body);
        } catch (e) {
            body = {};
        }
    }

    const name = body && (body.sender_name || body.name);
    const email = body && body.email;
    const content = body && (body.content || body.message);

    if (name && email && content) {
        context.res = {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
            body: { success: true, message: 'Message received successfully!' }
        };
    } else {
        context.res = {
            status: 400,
            headers: { 'Content-Type': 'application/json' },
            body: { success: false, error: 'Please provide all required fields.' }
        };
    }
};
