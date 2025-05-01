import { api } from ".";

class RentalClassService {
  async getAll() {
    return api.get("/rental-classes/");
  }

  async getById(id) {
    return api.get(`/rental-classes/${id}`);
  }

  async create(payload) {
    return api.post("/rental-classes/", payload);
  }

  async update(id, payload) {
    return api.patch(`/rental-classes/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/rental-classes/${id}`);
  }
}

class CarBrandService {
  async getAll() {
    return api.get("/car-brands/");
  }

  async getById(id) {
    return api.get(`/car-brands/${id}`);
  }

  async create(payload) {
    return api.post("/car-brands/", payload);
  }

  async update(id, payload) {
    return api.patch(`/car-brands/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/car-brands/${id}`);
  }
}

class TransmissionService {
  async getAll() {
    return api.get("/transmissions/");
  }

  async getById(id) {
    return api.get(`/transmissions/${id}`);
  }

  async create(payload) {
    return api.post("/transmissions/", payload);
  }

  async update(id, payload) {
    return api.patch(`/transmissions/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/transmissions/${id}`);
  }
}

class CarBodyService {
  async getAll() {
    return api.get("/car-bodies/");
  }

  async getById(id) {
    return api.get(`/car-bodies/${id}`);
  }

  async create(payload) {
    return api.post("/car-bodies/", payload);
  }

  async update(id, payload) {
    return api.patch(`/car-bodies/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/car-bodies/${id}`);
  }
}

class EngineTypeService {
  async getAll() {
    return api.get("/engine-types/");
  }

  async getById(id) {
    return api.get(`/engine-types/${id}`);
  }

  async create(payload) {
    return api.post("/engine-types/", payload);
  }

  async update(id, payload) {
    return api.patch(`/engine-types/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/engine-types/${id}`);
  }
}

class DriveTypeService {
  async getAll() {
    return api.get("/drive-type/");
  }

  async getById(id) {
    return api.get(`/drive-type/${id}`);
  }

  async create(payload) {
    return api.post("/drive-type/", payload);
  }

  async update(id, payload) {
    return api.patch(`/drive-type/${id}`, payload);
  }

  async delete(id) {
    return api.delete(`/drive-type/${id}`);
  }
}

export const rentalClassService = new RentalClassService();
export const carBrandService = new CarBrandService();
export const transmissionService = new TransmissionService();
export const carBodyService = new CarBodyService();
export const engineTypeService = new EngineTypeService();
export const driveTypeService = new DriveTypeService();