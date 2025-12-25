import { checkStatus } from "../checkStatus";

describe("checkStatus", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("UT-4: successful status retrieval", async () => {
    const mockReport = {
      application_id: 55,
      eligible: false,
      failed_checks: ["age"],
      external_reports: {}
    };

    global.fetch = jest.fn().mockResolvedValue({
      status: 200,
      json: async () => mockReport
    } as any);

    const result = await checkStatus(55);

    expect(fetch).toHaveBeenCalledWith("/api/status/55");
    expect(result).toEqual(mockReport);
  });

  test("UT-5: application not found", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      status: 404
    } as any);

    const result = await checkStatus(999);

    expect(result).toEqual({ status: "not_found" });
  });
});

import { mapServerResponseToViewModel } from "../src/mappers/mapServerResponseToViewModel";

describe("mapServerResponseToViewModel", () => {

  test("UT-6: correct mapping of full EligibilityReport", () => {
    const serverJson = {
      application_id: 55,
      eligible: true,
      failed_checks: [],
      external_reports: {
        mvd: { criminal_record: false },
        fns: { tax_debt: false }
      }
    };

    const result = mapServerResponseToViewModel(serverJson);

    expect(result).toEqual({
      status: "approved",
      eligible: true,
      failedChecks: [],
      externalReports: {
        mvd: { criminal_record: false },
        fns: { tax_debt: false }
      }
    });
  });

  test("UT-7: no failed checks in server response", () => {
    const serverJson = {
      application_id: 56,
      eligible: false,
      external_reports: {
        mvd: { criminal_record: true }
      }
    };

    const result = mapServerResponseToViewModel(serverJson);

    expect(result.failedChecks).toEqual([]);
    expect(result.failedChecks).not.toBeUndefined();
    expect(result.failedChecks).not.toBeNull();
  });

});

