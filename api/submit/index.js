cmodule.exports = async function (context, req) {
    context.log('Contact form API triggered.');

    const name = req.body && req.body.sender_name;
    const email = req.body && req.body.email;
    const content = req.body && req.body.content;

    if (name && email && content) {
        context.res = {
            status: 200,
            body: { success: true, message: 'Message received successfully!' }
        };
    } else {
        context.res = {
            status: 400,
            body: { success: false, error: 'Please provide all required fields.' }
        };
    }
};
