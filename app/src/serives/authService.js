import { api } from "./index.js";

class AuthService {
    async login(username, password) {
        const params = new  URLSearchParams();
        params.append('grant_type', 'password');
        params.append('username', username);
        params.append('password', password);
        
        try {
            const response = await api.post("/auth/login", params, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            });
            return response.data.access_token;
        } catch (error) {
            console.error(error);
        }
    }

    async fetchMe() {
        try {
            const response = await api.get("/users/me");
            return response.data;
        } catch(error) {
            console.error(error);
        }
    }
}

const authService = new AuthService();
export default authService;