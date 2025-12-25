import { submitApplication } from "../../../src/api/submitApplication";
import { uploadDocuments } from "../../../src/api/uploadDocuments";
import { checkStatus } from "../../../src/api/checkStatus";

describe("Frontend security: input sanitization and access control", () => {

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("malicious input does not cause XSS and is rejected by backend", async () => {
    const personalData = {
      fullName: "<script>alert('XSS')</script>",
      passport: "1234567890",
      taxId: "123456789012"
    };

    global.fetch = jest.fn().mockResolvedValue({
      status: 400,
      json: async () => ({ status: "error", reason: "invalid_input" })
    } as any);

    const result = await submitApplication(personalData, []);

    expect(result.status).toBe("error");
    expect(document.body.innerHTML).not.toContain("<script>");
  });

  test("invalid documents are rejected on upload", async () => {
    const files = [
      new File(["binary"], "virus.exe", { type: "application/octet-stream" }),
      new File([new ArrayBuffer(25 * 1024 * 1024)], "large.pdf", { type: "application/pdf" })
    ];

    const result = uploadDocuments(files);

    expect(result.success).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  test("user cannot access another user's application status", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      status: 403
    } as any);

    const response = await checkStatus(999);

    expect(response).toEqual({ status: "forbidden" });
  });

});
