import { submitApplication } from "../submitApplication";

describe("submitApplication", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });


  test("UT-1: successful application submit", async () => {
    const mockResponse = {
      status: "ok",
      applicationId: 55
    };

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => mockResponse
    } as any);

    const personalData = {
      fullName: "Иванов Иван",
      passport: "1234567890",
      taxId: "123456789012"
    };

    const files = [new File(["dummy"], "file1.png")];

    const result = await submitApplication(personalData, files);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(result).toEqual({
      status: "success",
      applicationId: 55
    });
  });


  test("UT-2: validation error from backend", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      json: async () => ({
        status: "error",
        fields: ["taxId"]
      })
    } as any);

    const personalData = {
      fullName: "Иванов Иван",
      passport: "1234567890"
    };

    const result = await submitApplication(personalData, []);

    expect(result).toEqual({
      status: "error",
      fields: ["taxId"]
    });
  });

  test("UT-3: network error during submit", async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error("Network down"));

    const personalData = {
      fullName: "Иванов Иван",
      passport: "1234567890",
      taxId: "123456789012"
    };

    const result = await submitApplication(personalData, []);

    expect(result).toEqual({
      status: "error",
      message: "network_error"
    });
  });
});
