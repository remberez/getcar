import { api } from ".";

class UserService {
    async updateProfile({ email, phone, full_name }) {
        try {
            const data = await api.patch("/users/me", {
                email,
                phone,
                full_name,
            })
        } catch (error) {
            console.error(error);
        }
    }
  }
  
  const userService = new UserService();
  export default userService;