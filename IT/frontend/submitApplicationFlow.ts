import { submitApplication } from "../../../src/api/submitApplication";

describe("Application submission integration", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("frontend sends valid data and receives 201", async () => {
    const personalData = {
      fullName: "Иванов Иван",
      birthDate: "1990-05-12",
      passport: "1234567890",
      taxId: "123456789012",
      address: "Москва"
    };

    const documents = ["passport", "medical_certificate"];

    global.fetch = jest.fn().mockResolvedValue({
      status: 201,
      json: async () => ({ applicationId: 55 })
    } as any);

    const result = await submitApplication(personalData, documents);

    expect(fetch).toHaveBeenCalled();
    expect(result.applicationId).toBe(55);
  });
});
