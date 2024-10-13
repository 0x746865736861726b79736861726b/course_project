async function authenticate() {
    if (typeof window.ethereum === 'undefined') {
        alert('Please install MetaMask!');
        return;
    }

    try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const userAddress = accounts[0];

        const message = 'Sign this message to authenticate';
        const signature = await window.ethereum.request({
            method: 'personal_sign',
            params: [message, userAddress],
        });

        const response = await fetch('/auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                user_address: userAddress,
                signature: signature,
                message: message,
            }),
        });
        const text = await response.text();
        console.log(text);
        const data = await response.json();
        if (response.ok) {
            console.log('Authenticated role:', data.role);
        } else {
            console.error('Authentication failed:', data.error);
        }
    } catch (error) {
        console.error('Error during authentication:', error);
    }
}
