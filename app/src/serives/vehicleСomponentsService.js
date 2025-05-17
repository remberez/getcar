import { api } from ".";

class RentalClassService {
  async getAll() {
    return (await api.get("/rental-classes/")).data;
  }

  async getById(id) {
    return (await api.get(`/rental-classes/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/rental-classes/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/rental-classes/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/rental-classes/${id}`)).data;
  }
}

class CarBrandService {
  async getAll() {
    return (await api.get("/car-brands/")).data;
  }

  async getById(id) {
    return (await api.get(`/car-brands/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/car-brands/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/car-brands/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/car-brands/${id}`)).data;
  }
}

class TransmissionService {
  async getAll() {
    return (await api.get("/transmissions/")).data;
  }

  async getById(id) {
    return (await api.get(`/transmissions/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/transmissions/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/transmissions/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/transmissions/${id}`)).data;
  }
}

class CarBodyService {
  async getAll() {
    return (await api.get("/car-bodies/")).data;
  }

  async getById(id) {
    return (await api.get(`/car-bodies/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/car-bodies/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/car-bodies/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/car-bodies/${id}`)).data;
  }
}

class EngineTypeService {
  async getAll() {
    return (await api.get("/engine-types/")).data;
  }

  async getById(id) {
    return (await api.get(`/engine-types/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/engine-types/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/engine-types/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/engine-types/${id}`)).data;
  }
}

class DriveTypeService {
  async getAll() {
    return (await api.get("/drive-type/")).data;
  }

  async getById(id) {
    return (await api.get(`/drive-type/${id}`)).data;
  }

  async create(payload) {
    return (await api.post("/drive-type/", payload)).data;
  }

  async update(id, payload) {
    return (await api.patch(`/drive-type/${id}`, payload)).data;
  }

  async delete(id) {
    return (await api.delete(`/drive-type/${id}`)).data;
  }
}

export const rentalClassService = new RentalClassService();
export const carBrandService = new CarBrandService();
export const transmissionService = new TransmissionService();
export const carBodyService = new CarBodyService();
export const engineTypeService = new EngineTypeService();
export const driveTypeService = new DriveTypeService();