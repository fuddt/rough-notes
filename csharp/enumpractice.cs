using System;
using System.Reflection;

public static class EnumExtensions
{

using System.ComponentModel;

public enum RaceType
{
    [Description("芝")]
    Turf,

    [Description("ダート")]
    Dirt,

    [Description("障害")]
    Steeplechase
}
    public static string GetDescription(this Enum value)
    {
        var field = value.GetType().GetField(value.ToString());
        var attribute = (DescriptionAttribute)Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute));
        return attribute?.Description ?? value.ToString();
    }
}