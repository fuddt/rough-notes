using System;
using System.Numerics;

public static class BreakJudge3Pt
{
    public static bool IsBreak(Vector2[] points, int i, double thetaThresholdDeg, out double thetaDeg)
    {
        thetaDeg = double.NaN;

        // i-1, i, i+1 が必要
        if (i <= 0 || i >= points.Length - 1)
            return false; // 判定不能は連続扱い（保守的）

        Vector2 v1 = points[i] - points[i - 1];
        Vector2 v2 = points[i + 1] - points[i];

        double theta = AngleBetween(v1, v2);
        if (double.IsNaN(theta))
            return false;

        thetaDeg = RadiansToDegrees(theta);
        return theta > DegreesToRadians(thetaThresholdDeg);
    }

    // 2ベクトルのなす角 [0..π]
    private static double AngleBetween(Vector2 v1, Vector2 v2)
    {
        double n1 = v1.Length();
        double n2 = v2.Length();
        if (n1 < 1e-12 || n2 < 1e-12)
            return double.NaN;

        double dot = (v1.X * v2.X + v1.Y * v2.Y) / (n1 * n2);
        dot = Math.Clamp(dot, -1.0, 1.0);
        return Math.Acos(dot);
    }

    private static double DegreesToRadians(double deg) => deg * Math.PI / 180.0;
    private static double RadiansToDegrees(double rad) => rad * 180.0 / Math.PI;
}