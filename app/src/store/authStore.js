import { makeAutoObservable } from "mobx";
import authService from "../serives/authService";

class AuthStore {
    isAuth = false;
    user = {};
    isLoading = null;

    constructor() {
        makeAutoObservable(this);
    }

    setIsAuth(value) {
        this.isAuth = value;
    }

    setToken(token) {
        if (token) {
            localStorage.setItem("token", token);
            this.setIsAuth(true);
        } else {
            localStorage.removeItem("token");
        }
    }

    async setUser() {
        this.isLoading = true;
        try {
            const data = await authService.fetchMe();
            if (data) {
                this.user = data;
                this.setIsAuth(true);
            } else {
                this.user = {};
                this.setIsAuth(false);
            }
        } catch {
            this.user = {};
            this.setIsAuth(false);
        } finally {
            this.isLoading = false;
        }
    }
}

const authStore = new AuthStore();
export default authStore;