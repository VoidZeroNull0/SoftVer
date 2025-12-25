import { checkStatus } from "../../../src/api/checkStatus";
import { mapServerResponseToViewModel } from "../../../src/mappers/mapServerResponseToViewModel";

describe("Status display integration", () => {
  test("status is loaded and mapped correctly", async () => {
    const serverJson = {
      application_id: 55,
      eligible: false,
      failed_checks: ["criminal_record"],
      external_reports: {}
    };

    global.fetch = jest.fn().mockResolvedValue({
      status: 200,
      json: async () => serverJson
    } as any);

    const response = await checkStatus(55);
    const viewModel = mapServerResponseToViewModel(response);

    expect(viewModel.status).toBe("rejected");
    expect(viewModel.failedChecks).toEqual(["criminal_record"]);
  });
});
